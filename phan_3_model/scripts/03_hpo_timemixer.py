"""
03_hpo_timemixer.py

HPO for TimeMixer.
Objective: minimize MAE on the final 548 timesteps.
"""
from __future__ import annotations

import argparse
import json
import os
import random
from pathlib import Path

import numpy as np
import optuna
import pandas as pd
import torch
import yaml
from sklearn.metrics import mean_absolute_error

from neuralforecast import NeuralForecast
from neuralforecast.models import TimeMixer
from neuralforecast.losses.pytorch import MAE as NFMAE

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CFG = yaml.safe_load(open(PROJECT_ROOT / "config" / "general.yaml", "r", encoding="utf-8"))

SEED = int(CFG.get("seed", 42))
HOLDOUT = int(CFG.get("horizon", 548))
PROC_DIR = PROJECT_ROOT / CFG["processed_dir"]
ARTIFACT_DIR = PROJECT_ROOT / CFG.get("artifacts_dir", "artifacts")


def set_all_seeds(seed: int = 42) -> None:
    random.seed(seed)
    os.environ["PYTHONHASHSEED"] = str(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False


set_all_seeds(SEED)

def optimize_target(target: str, n_trials: int) -> None:
    path = PROC_DIR / f"{target}_temporal.csv"
    df = pd.read_csv(path, parse_dates=["ds"]).sort_values("ds").reset_index(drop=True)
    if len(df) <= HOLDOUT:
        raise ValueError(f"{path} needs > {HOLDOUT} rows.")

    train_df = df.iloc[:-HOLDOUT].copy()
    val_df = df.iloc[-HOLDOUT:].copy()

    if target == "revenue":
        train_df["y_model"] = np.log1p(train_df["y"])
        val_true = val_df["y"].values
    else:
        train_df["y_model"] = train_df["y"]
        val_true = val_df["y"].values

    nf_train = train_df[["unique_id", "ds", "y_model"]].rename(columns={"y_model": "y"})

    def objective(trial: optuna.Trial) -> float:
        cfg = {
            "n_series": 1,
            "input_size": trial.suggest_categorical("input_size", [364, HOLDOUT, 728, 1096]),
            "d_model": trial.suggest_categorical("d_model", [16, 32, 64]),
            "d_ff": trial.suggest_categorical("d_ff", [16, 32, 64]),
            "down_sampling_layers": trial.suggest_categorical("down_sampling_layers", [1, 2]),
            "learning_rate": trial.suggest_float("learning_rate", 1e-4, 1e-2, log=True),
            "dropout": trial.suggest_float("dropout", 0.3, 0.5, log=True),
            "max_steps": trial.suggest_int("max_steps", 200, 1500, step=100),
            "batch_size": trial.suggest_categorical("batch_size", [32, 64, 128]),
            "scaler_type": trial.suggest_categorical("scaler_type", ["robust", "standard", "identity"]),
            "random_seed": SEED,
        }

        model = TimeMixer(h=HOLDOUT, loss=NFMAE(), valid_loss=NFMAE(), **cfg)
        nf = NeuralForecast(models=[model], freq="D")
        nf.fit(df=nf_train)
        pred = nf.predict().reset_index()
        col = next((c for c in pred.columns if c.lower().startswith("timemixer")), "TimeMixer")
        y_pred = pred[col].values
        
        # Cast to float64 to prevent float32 overflow
        y_pred = np.asarray(y_pred, dtype=np.float64)
        
        # Guard against NaNs and infs caused by exploding gradients in bad trials
        y_pred = np.nan_to_num(y_pred, nan=0.0, posinf=50.0, neginf=-50.0)
        
        if target == "revenue":
            # Prevent overflow in expm1, 50.0 is safe and large enough for log1p revenue
            y_pred = np.clip(y_pred, a_min=-50.0, a_max=50.0)
            y_pred = np.expm1(y_pred)
            
        return mean_absolute_error(val_true, y_pred)

    study = optuna.create_study(direction="minimize", sampler=optuna.samplers.TPESampler(seed=SEED))
    study.optimize(objective, n_trials=n_trials)
    best = study.best_params

    out = ARTIFACT_DIR / "best_configs" / f"timemixer_{target}.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        json.dump(best, f, indent=2)

    print(f"[{target}] best holdout MAE: {study.best_value:,.6f}")
    print(f"[{target}] saved: {out}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--n-trials", type=int, default=10)
    args = parser.parse_args()

    for tgt in ("revenue", "cogs_ratio"):
        optimize_target(tgt, n_trials=args.n_trials)
