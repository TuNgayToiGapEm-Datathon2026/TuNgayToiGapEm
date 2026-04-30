"""
05_visualize_results.py

Visualizes the last fold of the expanding window CV:
1. Revenue and COGS (Actual vs Predicted)
2. Feature importance for LightGBM (Main + Specialists)
"""
import json
import os
import random
from pathlib import Path

import lightgbm as lgb
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import torch
import yaml
from sklearn.metrics import mean_absolute_error, r2_score

from neuralforecast import NeuralForecast
from neuralforecast.models import TimeMixer
from neuralforecast.losses.pytorch import MAE as NFMAE

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CFG = yaml.safe_load(open(PROJECT_ROOT / "config" / "general.yaml", "r", encoding="utf-8"))

SEED = int(CFG.get("seed", 42))
PROC_DIR = PROJECT_ROOT / CFG["processed_dir"]
FEATURE_DIR = PROJECT_ROOT / CFG["features_dir"]
ARTIFACT_DIR = PROJECT_ROOT / CFG.get("artifacts_dir", "artifacts")
OUT_DIR = PROJECT_ROOT / "outputs" / "plots"
OUT_DIR.mkdir(parents=True, exist_ok=True)

def set_all_seeds(seed: int = 42) -> None:
    random.seed(seed)
    os.environ["PYTHONHASHSEED"] = str(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)

set_all_seeds(SEED)

def _load_json(path: Path) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def _feature_cols(df: pd.DataFrame) -> list[str]:
    drop_cols = {"unique_id", "ds", "y", "target", "y_rev"}
    return [c for c in df.columns if c not in drop_cols and pd.api.types.is_numeric_dtype(df[c])]

def _predict_prophet(train_df: pd.DataFrame, pred_dates: pd.Series) -> np.ndarray:
    from prophet import Prophet
    fit_df = train_df[train_df["ds"] >= pd.Timestamp("2019-01-01")][["ds", "y"]].copy()
    if len(fit_df) < 2:
        fit_df = train_df[["ds", "y"]].copy()
    m = Prophet(yearly_seasonality=True, weekly_seasonality=True, daily_seasonality=False)
    m.fit(fit_df)
    fc = m.predict(pd.DataFrame({"ds": pd.to_datetime(pred_dates)}))
    return fc["yhat"].values

def _predict_timemixer(train_df: pd.DataFrame, pred_len: int, cfg: dict, target: str) -> np.ndarray:
    work = train_df.copy()
    work["y_model"] = np.log1p(work["y"]) if target == "revenue" else work["y"]
    nf_train = work[["unique_id", "ds", "y_model"]].rename(columns={"y_model": "y"})
    model = TimeMixer(h=pred_len, loss=NFMAE(), valid_loss=NFMAE(), n_series=1, **cfg)
    nf = NeuralForecast(models=[model], freq="D")
    nf.fit(df=nf_train)
    pred = nf.predict().reset_index()
    col = next((c for c in pred.columns if c.lower().startswith("timemixer")), "TimeMixer")
    y_pred = pred[col].values
    return np.expm1(y_pred) if target == "revenue" else y_pred

def get_lgb_importance(train_df: pd.DataFrame, val_df: pd.DataFrame, cfg: dict, target: str):
    work = train_df.copy()
    work["target"] = np.log1p(work["y"]) if target == "revenue" else work["y"]
    feats = _feature_cols(work)
    X_tr, y_tr = work[feats], work["target"]
    base_w = np.where((work["ds"].dt.year <= 2018), 1.0, 0.2)
    
    alpha = float(cfg.get("alpha", 0.6))
    specialist_multiplier = float(cfg.get("specialist_multiplier", 2.0))
    params = {k: v for k, v in cfg.items() if k not in {"alpha", "specialist_multiplier"}}
    
    # Train Main
    main = lgb.LGBMRegressor(random_state=SEED, n_estimators=1000, verbose=-1, **params)
    main.fit(X_tr, y_tr, sample_weight=base_w)
    
    importances = {"main": pd.Series(main.feature_importances_, index=feats)}
    
    # Predict Main
    pred_main = main.predict(val_df[feats])
    final_pred = pred_main.copy()
    
    tr_q = work["ds"].dt.quarter.values
    val_q = val_df["ds"].dt.quarter.values
    
    for q in (1, 2, 3, 4):
        m = val_q == q
        if not m.any(): continue
        w_q = base_w.copy()
        w_q[tr_q == q] *= specialist_multiplier
        spec = lgb.LGBMRegressor(random_state=SEED, n_estimators=1000, verbose=-1, **params)
        spec.fit(X_tr, y_tr, sample_weight=w_q)
        importances[f"q{q}_specialist"] = pd.Series(spec.feature_importances_, index=feats)
        p_q = spec.predict(val_df[feats])
        final_pred[m] = alpha * p_q[m] + (1.0 - alpha) * pred_main[m]
        
    y_pred = np.expm1(final_pred) if target == "revenue" else final_pred
    return y_pred, importances

def plot_importance(importances: dict, title_prefix: str, target: str):
    for name, imp in importances.items():
        plt.figure(figsize=(10, 8))
        imp.sort_values(ascending=False).head(20).plot(kind="barh").invert_yaxis()
        plt.title(f"{title_prefix} - {name} Importance ({target})")
        plt.tight_layout()
        plt.savefig(OUT_DIR / f"importance_{target}_{name}.png", dpi=800)
        plt.close()

def main():
    # CV Settings from 04
    n_splits = 3
    step = 365
    horizon = 548
    w_ens = np.array([0.1, 0.2, 0.7]) # Default weights from 04
    
    # Load data
    rev_df = pd.read_csv(PROC_DIR / "revenue_temporal.csv", parse_dates=["ds"]).sort_values("ds")
    cogs_df = pd.read_csv(PROC_DIR / "cogs_ratio_temporal.csv", parse_dates=["ds"]).sort_values("ds")
    
    # Last fold indices
    N = len(rev_df)
    val_end = N
    val_start = val_end - horizon
    train_end = val_start
    
    # Folds for both
    train_rev = rev_df.iloc[:train_end].copy()
    val_rev = rev_df.iloc[val_start:val_end].copy()
    
    train_cogs = cogs_df.iloc[:train_end].copy()
    val_cogs = cogs_df.iloc[val_start:val_end].copy()
    
    # Load configs
    tm_cfg_rev = _load_json(ARTIFACT_DIR / "best_configs" / "timemixer_revenue.json")
    lgb_cfg_rev = _load_json(ARTIFACT_DIR / "best_configs" / "lgb_ensemble_revenue.json")
    tm_cfg_cogs = _load_json(ARTIFACT_DIR / "best_configs" / "timemixer_cogs_ratio.json")
    lgb_cfg_cogs = _load_json(ARTIFACT_DIR / "best_configs" / "lgb_ensemble_cogs_ratio.json")
    
    print("Predicting Revenue (Last Fold)...")
    p_rev = _predict_prophet(train_rev, val_rev["ds"])
    t_rev = _predict_timemixer(train_rev, horizon, tm_cfg_rev, "revenue")
    l_rev, imp_rev = get_lgb_importance(train_rev, val_rev, lgb_cfg_rev, "revenue")
    ens_rev = w_ens[0]*p_rev + w_ens[1]*t_rev + w_ens[2]*l_rev
    
    print("Predicting COGS Ratio (Last Fold)...")
    p_cogs_r = _predict_prophet(train_cogs, val_cogs["ds"])
    t_cogs_r = _predict_timemixer(train_cogs, horizon, tm_cfg_cogs, "cogs_ratio")
    l_cogs_r, imp_cogs = get_lgb_importance(train_cogs, val_cogs, lgb_cfg_cogs, "cogs_ratio")
    ens_cogs_r = w_ens[0]*p_cogs_r + w_ens[1]*t_cogs_r + w_ens[2]*l_cogs_r
    
    # Convert COGS to raw
    y_rev_true = val_rev["y"].values
    y_cogs_true = val_cogs["y"].values * y_rev_true
    
    # Using actual revenue for visualization of ratio performance
    ens_cogs_raw = ens_cogs_r * y_rev_true
    
    # Visualization: Revenue
    plt.figure(figsize=(12, 6))
    plt.plot(val_rev["ds"], y_rev_true, label="Actual Revenue", color="black", alpha=0.6)
    plt.plot(val_rev["ds"], ens_rev, label="Ensemble Prediction", color="blue")
    plt.fill_between(val_rev["ds"], y_rev_true, ens_rev, color="blue", alpha=0.1)
    plt.title(f"Revenue Forecast (Last Fold) - MAE: {mean_absolute_error(y_rev_true, ens_rev):.2f}")
    plt.legend()
    plt.savefig(OUT_DIR / "last_fold_revenue.png", dpi=800)
    plt.close()
    
    # Visualization: COGS
    plt.figure(figsize=(12, 6))
    plt.plot(val_rev["ds"], y_cogs_true, label="Actual COGS", color="black", alpha=0.6)
    plt.plot(val_rev["ds"], ens_cogs_raw, label="Ensemble Prediction", color="red")
    plt.fill_between(val_rev["ds"], y_cogs_true, ens_cogs_raw, color="red", alpha=0.1)
    plt.title(f"Raw COGS Forecast (Last Fold) - MAE: {mean_absolute_error(y_cogs_true, ens_cogs_raw):.2f}")
    plt.legend()
    plt.savefig(OUT_DIR / "last_fold_cogs.png", dpi=800)
    plt.close()
    
    # Combined View
    fig, ax = plt.subplots(2, 1, figsize=(14, 10), sharex=True)
    ax[0].plot(val_rev["ds"], y_rev_true, label="Actual Rev", color="gray")
    ax[0].plot(val_rev["ds"], ens_rev, label="Pred Rev", color="blue")
    ax[0].set_title("Revenue")
    ax[0].legend()
    
    ax[1].plot(val_rev["ds"], y_cogs_true, label="Actual COGS", color="gray")
    ax[1].plot(val_rev["ds"], ens_cogs_raw, label="Pred COGS", color="red")
    ax[1].set_title("Raw COGS")
    ax[1].legend()
    
    plt.tight_layout()
    plt.savefig(OUT_DIR / "last_fold_combined.png", dpi=800)
    plt.close()
    
    # Feature Importance
    print("Plotting Feature Importance...")
    plot_importance(imp_rev, "Revenue", "revenue")
    plot_importance(imp_cogs, "COGS Ratio", "cogs_ratio")
    
    print(f"Visualizations saved to: {OUT_DIR}")

if __name__ == "__main__":
    main()
