"""
02_hpo_lgb_ensemble.py

HPO for LightGBM ensemble (main + quarterly specialists).
Objective: minimize MAE on the final 548 timesteps.
"""
from __future__ import annotations

import argparse
import json
import os
import random
from pathlib import Path

import lightgbm as lgb
import numpy as np
import optuna
import pandas as pd
import torch
import yaml
from sklearn.metrics import mean_absolute_error

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


def _feature_cols(df: pd.DataFrame) -> list[str]:
    drop_cols = {"unique_id", "ds", "y", "target"}
    return [c for c in df.columns if c not in drop_cols and pd.api.types.is_numeric_dtype(df[c])]


def _train_lgb(X_tr, y_tr, w_tr, X_val, y_val, params):
    model = lgb.LGBMRegressor(
        random_state=SEED,
        n_estimators=1000,
        verbose=-1,
        **params,
    )
    model.fit(
        X_tr,
        y_tr,
        sample_weight=w_tr,
        eval_set=[(X_val, y_val)],
        callbacks=[lgb.early_stopping(100, verbose=False)],
    )
    return model


def optimize_target(target: str, n_trials: int) -> None:
    path = PROC_DIR / f"{target}_temporal.csv"
    df = pd.read_csv(path, parse_dates=["ds"]).sort_values("ds").reset_index(drop=True)
    if len(df) <= HOLDOUT:
        raise ValueError(f"{path} needs > {HOLDOUT} rows.")

    df["target"] = np.log1p(df["y"]) if target == "revenue" else df["y"]
    feats = _feature_cols(df)
    if not feats:
        raise ValueError(f"No numeric temporal features found for {target}.")

    train_df = df.iloc[:-HOLDOUT].copy()
    val_df = df.iloc[-HOLDOUT:].copy()
    X_tr, y_tr = train_df[feats], train_df["target"]
    X_val, y_val = val_df[feats], val_df["target"]

    base_weights = np.where((train_df["ds"].dt.year <= 2018), 1.0, 0.2)
    tr_quarter = train_df["ds"].dt.quarter.values
    val_quarter = val_df["ds"].dt.quarter.values

    def objective(trial: optuna.Trial) -> float:
        params = {
            "learning_rate": trial.suggest_float("learning_rate", 0.005, 0.08, log=True),
            "num_leaves": trial.suggest_int("num_leaves", 16, 192),
            "max_depth": trial.suggest_int("max_depth", 3, 12),
            "min_child_samples": trial.suggest_int("min_child_samples", 5, 120),
            "subsample": trial.suggest_float("subsample", 0.6, 1.0),
            "colsample_bytree": trial.suggest_float("colsample_bytree", 0.6, 1.0),
            "reg_alpha": trial.suggest_float("reg_alpha", 1e-8, 10.0, log=True),
            "reg_lambda": trial.suggest_float("reg_lambda", 1e-8, 10.0, log=True),
        }
        alpha = trial.suggest_float("alpha", 0.2, 0.75)
        specialist_multiplier = trial.suggest_float("specialist_multiplier", 1.1, 3.0)

        main = _train_lgb(X_tr, y_tr, base_weights, X_val, y_val, params)
        pred_main = main.predict(X_val)
        pred = pred_main.copy()

        for q in (1, 2, 3, 4):
            m = val_quarter == q
            if not m.any():
                continue
            w_q = base_weights.copy()
            w_q[tr_quarter == q] *= specialist_multiplier
            spec = _train_lgb(X_tr, y_tr, w_q, X_val, y_val, params)
            pred_q = spec.predict(X_val)
            pred[m] = alpha * pred_q[m] + (1.0 - alpha) * pred_main[m]

        pred_raw = np.expm1(pred) if target == "revenue" else pred
        return mean_absolute_error(val_df["y"].values, pred_raw)

    study = optuna.create_study(direction="minimize", sampler=optuna.samplers.TPESampler(seed=SEED))
    study.optimize(objective, n_trials=n_trials)
    best = study.best_params

    out = ARTIFACT_DIR / "best_configs" / f"lgb_ensemble_{target}.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        json.dump(best, f, indent=2)

    print(f"[{target}] best holdout MAE: {study.best_value:,.6f}")
    print(f"[{target}] saved: {out}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--n-trials", type=int, default=100)
    args = parser.parse_args()

    for tgt in ("revenue", "cogs_ratio"):
        optimize_target(tgt, n_trials=args.n_trials)
