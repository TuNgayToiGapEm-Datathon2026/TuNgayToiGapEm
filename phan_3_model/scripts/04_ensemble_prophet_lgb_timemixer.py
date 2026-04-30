"""
04_ensemble_prophet_lgb_timemixer.py

Final ensemble of:
- Prophet (fit only on ds >= 2019-01-01)
- best LightGBM ensemble config from script 02
- best TimeMixer config from script 03

Fixed weight ensemble.
"""
from __future__ import annotations

import argparse
import json
import os
import random
from pathlib import Path

import lightgbm as lgb
import numpy as np
import pandas as pd
import torch
import yaml
from sklearn.metrics import mean_absolute_error, r2_score, mean_squared_error

from neuralforecast import NeuralForecast
from neuralforecast.models import TimeMixer
from neuralforecast.losses.pytorch import MAE as NFMAE

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CFG = yaml.safe_load(open(PROJECT_ROOT / "config" / "general.yaml", "r", encoding="utf-8"))

SEED = int(CFG.get("seed", 42))
HOLDOUT = int(CFG.get("horizon", 548))
PROC_DIR = PROJECT_ROOT / CFG["processed_dir"]
FEATURE_DIR = PROJECT_ROOT / CFG["features_dir"]
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



def _load_json(path: Path) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _feature_cols(df: pd.DataFrame) -> list[str]:
    drop_cols = {"unique_id", "ds", "y", "target"}
    return [c for c in df.columns if c not in drop_cols and pd.api.types.is_numeric_dtype(df[c])]


def _temporal_cols(df: pd.DataFrame) -> list[str]:
    """Return columns that are temporal features (everything except id/ds/y)."""
    drop_cols = {"unique_id", "ds", "y", "target"}
    return [c for c in df.columns if c not in drop_cols and pd.api.types.is_numeric_dtype(df[c])]


def _predict_prophet(train_df: pd.DataFrame, pred_dates: pd.Series) -> np.ndarray:
    from prophet import Prophet

    # Use 2019 filter if possible, otherwise use all training data
    fit_df = train_df[train_df["ds"] >= pd.Timestamp("2019-01-01")][["ds", "y"]].copy()
    if len(fit_df) < 2:
        fit_df = train_df[["ds", "y"]].copy()
    m = Prophet(
        yearly_seasonality=True,
        weekly_seasonality=True,
        daily_seasonality=False,
        changepoint_prior_scale=0.1,
        seasonality_prior_scale=15.0,
        changepoint_range=0.95,
    )
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


def _predict_lgb_ensemble(train_df: pd.DataFrame, pred_feat: pd.DataFrame, cfg: dict, target: str) -> np.ndarray:
    work = train_df.copy()
    work["target"] = np.log1p(work["y"]) if target == "revenue" else work["y"]
    feats = [c for c in _feature_cols(work) if c in pred_feat.columns]
    X_tr = work[feats]
    y_tr = work["target"]
    base_w = np.where((work["ds"].dt.year <= 2018), 1.0, 0.2)

    alpha = float(cfg.get("alpha", 0.6))
    specialist_multiplier = float(cfg.get("specialist_multiplier", 2.0))
    params = {k: v for k, v in cfg.items() if k not in {"alpha", "specialist_multiplier"}}

    main = lgb.LGBMRegressor(random_state=SEED, n_estimators=1000, verbose=-1, **params)
    main.fit(X_tr, y_tr, sample_weight=base_w)
    X_pred = pred_feat[feats]
    pred_main = main.predict(X_pred)
    pred = pred_main.copy()

    tr_q = work["ds"].dt.quarter.values
    pred_q = pd.to_datetime(pred_feat["ds"]).dt.quarter.values
    for q in (1, 2, 3, 4):
        m = pred_q == q
        if not m.any():
            continue
        w_q = base_w.copy()
        w_q[tr_q == q] *= specialist_multiplier
        spec = lgb.LGBMRegressor(random_state=SEED, n_estimators=1000, verbose=-1, **params)
        spec.fit(X_tr, y_tr, sample_weight=w_q)
        p_q = spec.predict(X_pred)
        pred[m] = alpha * p_q[m] + (1.0 - alpha) * pred_main[m]

    return np.expm1(pred) if target == "revenue" else pred


def evaluate_cv(df: pd.DataFrame, target: str, tm_cfg: dict, lgb_cfg: dict, w: np.ndarray, n_splits=3, step=365, horizon=548):
    print(f"\n--- Running {n_splits}-fold CV for {target} ---")
    
    # If cogs_ratio, we calculate metrics on raw COGS by merging with revenue
    is_cogs = (target == "cogs_ratio")
    if is_cogs:
        rev_df = pd.read_csv(PROC_DIR / "revenue_temporal.csv", parse_dates=["ds"])[["ds", "y"]]
        df = df.merge(rev_df, on="ds", suffixes=("", "_rev"))

    N = len(df)
    maes = {"prophet": [], "timemixer": [], "lgbm": [], "ensemble": []}
    mses = {"prophet": [], "timemixer": [], "lgbm": [], "ensemble": []}
    r2s = {"prophet": [], "timemixer": [], "lgbm": [], "ensemble": []}
    
    for i in range(n_splits):
        offset = (n_splits - 1 - i) * step
        val_end = N - offset
        val_start = val_end - horizon
        train_end = val_start
        
        train_df = df.iloc[:train_end].copy()
        val_df = df.iloc[val_start:val_end].copy()
        
        print(f"\nFold {i}: Train ends at {train_df['ds'].max().date()}, Val: {val_df['ds'].min().date()} to {val_df['ds'].max().date()}")
        
        prophet_f = _predict_prophet(train_df, val_df["ds"])
        tm_f = _predict_timemixer(train_df, len(val_df), tm_cfg, target)
        lgb_f = _predict_lgb_ensemble(train_df, val_df, lgb_cfg, target)
        
        ens_f = w[0] * prophet_f + w[1] * tm_f + w[2] * lgb_f
        
        y_true = val_df["y"].values
        y_rev = val_df["y_rev"].values if is_cogs else 1.0
        
        for name, pred in [("prophet", prophet_f), ("timemixer", tm_f), ("lgbm", lgb_f), ("ensemble", ens_f)]:
            # If cogs_ratio, convert to raw units for evaluation
            maes[name].append(mean_absolute_error(y_true * y_rev, pred * y_rev))
            mses[name].append(mean_squared_error(y_true * y_rev, pred * y_rev))
            r2s[name].append(r2_score(y_true * y_rev, pred * y_rev))
        
        unit = "Raw COGS" if is_cogs else "Value"
        print(f"  Prophet   | MAE: {maes['prophet'][-1]:.4f} | MSE: {mses['prophet'][-1]:.4f} | R2: {r2s['prophet'][-1]:.4f} ({unit})")
        print(f"  TimeMixer | MAE: {maes['timemixer'][-1]:.4f} | MSE: {mses['timemixer'][-1]:.4f} | R2: {r2s['timemixer'][-1]:.4f} ({unit})")
        print(f"  LGBM      | MAE: {maes['lgbm'][-1]:.4f} | MSE: {mses['lgbm'][-1]:.4f} | R2: {r2s['lgbm'][-1]:.4f} ({unit})")
        print(f"  Ensemble  | MAE: {maes['ensemble'][-1]:.4f} | MSE: {mses['ensemble'][-1]:.4f} | R2: {r2s['ensemble'][-1]:.4f} ({unit})")
        
    print(f"\n=== CV Summary for {target} ===")
    models = ["prophet", "timemixer", "lgbm", "ensemble"]
    rows = []
    unit_label = "Raw COGS" if is_cogs else target.capitalize()
    for m in models:
        print(f"Model: {m.capitalize()} ({unit_label})")
        for i in range(n_splits):
            print(f"  Fold {i} MAE: {maes[m][i]:.4f} | MSE: {mses[m][i]:.4f} | R2: {r2s[m][i]:.4f}")
            rows.append({
                "target": target, "model": m, "fold": i, "unit": unit_label,
                "mae": maes[m][i], "mse": mses[m][i], "r2": r2s[m][i]
            })
        m_mae, m_mse, m_r2 = np.mean(maes[m]), np.mean(mses[m]), np.mean(r2s[m])
        print(f"  MEAN   MAE: {m_mae:.4f} | MSE: {m_mse:.4f} | R2: {m_r2:.4f}\n")
        rows.append({
            "target": target, "model": m, "fold": "MEAN", "unit": unit_label,
            "mae": m_mae, "mse": m_mse, "r2": m_r2
        })
    
    cv_res_df = pd.DataFrame(rows)
    out_path = ARTIFACT_DIR / f"cv_results_{target}.csv"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    cv_res_df.to_csv(out_path, index=False)
    print(f"Saved CV results to {out_path}")
    print("-" * 40)


def _predict_future(df: pd.DataFrame, target: str, tm_cfg: dict, lgb_cfg: dict) -> pd.DataFrame:
    fut = pd.read_csv(FEATURE_DIR / "temporal_xreg_future.csv", parse_dates=["ds"])
    prophet_f = _predict_prophet(df, fut["ds"])
    tm_f = _predict_timemixer(df, len(fut), tm_cfg, target)
    lgb_f = _predict_lgb_ensemble(df, fut, lgb_cfg, target)
    return pd.DataFrame({"ds": fut["ds"], "prophet": prophet_f, "timemixer": tm_f, "lgbm": lgb_f})


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--w-prophet", type=float, default=0.1)
    parser.add_argument("--w-timemixer", type=float, default=0.2)
    parser.add_argument("--w-lgbm", type=float, default=0.7)
    args = parser.parse_args()

    out_dir = PROJECT_ROOT / "outputs"
    out_dir.mkdir(parents=True, exist_ok=True)

    results = {}
    for target in ("revenue", "cogs_ratio"):
        df = pd.read_csv(PROC_DIR / f"{target}_temporal.csv", parse_dates=["ds"]).sort_values("ds")
        tm_cfg = _load_json(ARTIFACT_DIR / "best_configs" / f"timemixer_{target}.json")
        lgb_cfg = _load_json(ARTIFACT_DIR / "best_configs" / f"lgb_ensemble_{target}.json")

        s = args.w_prophet + args.w_timemixer + args.w_lgbm
        w = np.array([args.w_prophet, args.w_timemixer, args.w_lgbm], dtype=float) / s
        
        evaluate_cv(df, target, tm_cfg, lgb_cfg, w, n_splits=3, step=365, horizon=548)

        base_future = _predict_future(df, target, tm_cfg, lgb_cfg)

        y_pred = (
            w[0] * base_future["prophet"].values
            + w[1] * base_future["timemixer"].values
            + w[2] * base_future["lgbm"].values
        )

        results[target] = pd.DataFrame({"ds": base_future["ds"], "pred": y_pred})
        base_future.to_csv(out_dir / f"base_future_{target}.csv", index=False)

    final = results["revenue"][["ds"]].copy()
    final["Revenue"] = results["revenue"]["pred"].values
    final["COGS"] = results["cogs_ratio"]["pred"].values * final["Revenue"].values
    final = final.rename(columns={"ds": "Date"})
    out_path = out_dir / "final_prediction.csv"
    final.to_csv(out_path, index=False)
    print(f"Saved: {out_path}")
