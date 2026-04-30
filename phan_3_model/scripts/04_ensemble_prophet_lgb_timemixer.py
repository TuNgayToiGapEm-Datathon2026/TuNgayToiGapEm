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


def _predict_prophet(train_df: pd.DataFrame, pred_dates: pd.Series) -> pd.DataFrame:
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
    return fc[["yhat", "yhat_lower", "yhat_upper"]]


def _predict_timemixer(train_df: pd.DataFrame, cfg: dict, target: str) -> np.ndarray:
    work = train_df.copy()
    if target == "revenue":
        work["y_model"] = np.log1p(work["y"])
    else:
        work["y_model"] = work["y"]
    
    nf_train = work[["unique_id", "ds", "y_model"]].rename(columns={"y_model": "y"})
    
    model = TimeMixer(n_series=1, h=HOLDOUT, loss=NFMAE(), valid_loss=NFMAE(), random_seed=SEED, **cfg)
    nf = NeuralForecast(models=[model], freq="D")
    nf.fit(df=nf_train)
    pred = nf.predict().reset_index()
    col = next((c for c in pred.columns if c.lower().startswith("timemixer")), "TimeMixer")
    y_pred = pred[col].values
    
    if target == "revenue":
        y_pred = np.clip(y_pred, a_min=-50.0, a_max=50.0)
        y_pred = np.expm1(y_pred)
    
    return np.asarray(y_pred, dtype=np.float64)


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


def evaluate_cv(df: pd.DataFrame, target: str, lgb_cfg: dict, w: np.ndarray, n_splits=3, step=365, horizon=548):
    print(f"\n--- Running {n_splits}-fold CV for {target} ---")
    
    # If cogs_ratio, we calculate metrics on raw COGS by merging with revenue
    is_cogs = (target == "cogs_ratio")
    if is_cogs:
        rev_df = pd.read_csv(PROC_DIR / "revenue_temporal.csv", parse_dates=["ds"])[["ds", "y"]]
        df = df.merge(rev_df, on="ds", suffixes=("", "_rev"))

    N = len(df)
    maes = {"prophet": [], "timemixer": [], "lgbm": [], "ensemble": []}
    mses = {"prophet": [], "timemixer": [], "lgbm": [], "ensemble": []}
    rmses = {"prophet": [], "timemixer": [], "lgbm": [], "ensemble": []}
    r2s = {"prophet": [], "timemixer": [], "lgbm": [], "ensemble": []}
    
    # Store CI percentages for Prophet (3 periods)
    ci_p1 = [] # 1-90
    ci_p2 = [] # 91-365
    ci_p3 = [] # 366-548
    
    for i in range(n_splits):
        offset = (n_splits - 1 - i) * step
        val_end = N - offset
        val_start = val_end - horizon
        train_end = val_start
        
        train_df = df.iloc[:train_end].copy()
        val_df = df.iloc[val_start:val_end].copy()
        
        print(f"\nFold {i}: Train ends at {train_df['ds'].max().date()}, Val: {val_df['ds'].min().date()} to {val_df['ds'].max().date()}")
        
        prophet_fc = _predict_prophet(train_df, val_df["ds"])
        prophet_f = prophet_fc["yhat"].values
        tm_f = _predict_timemixer(train_df, lgb_cfg["timemixer"], target)
        lgb_f = _predict_lgb_ensemble(train_df, val_df, lgb_cfg["lgbm"], target)
        
        ens_f = w[0] * prophet_f + w[1] * tm_f + w[2] * lgb_f
        
        # Calculate CI % for Prophet
        yhat = prophet_fc["yhat"].values
        y_low = prophet_fc["yhat_lower"].values
        y_hi = prophet_fc["yhat_upper"].values
        # Handle zero division just in case
        ci_pct = np.where(yhat != 0, (y_hi - y_low) / yhat, 0.0)
        
        ci_p1.append(np.mean(ci_pct[0:90]))
        ci_p2.append(np.mean(ci_pct[90:365]))
        ci_p3.append(np.mean(ci_pct[365:548]))
        
        y_true = val_df["y"].values
        y_rev = val_df["y_rev"].values if is_cogs else 1.0
        
        for name, pred in [("prophet", prophet_f), ("timemixer", tm_f), ("lgbm", lgb_f), ("ensemble", ens_f)]:
            # If cogs_ratio, convert to raw units for evaluation
            mae_val = mean_absolute_error(y_true * y_rev, pred * y_rev)
            mse_val = mean_squared_error(y_true * y_rev, pred * y_rev)
            rmse_val = np.sqrt(mse_val)
            r2_val = r2_score(y_true * y_rev, pred * y_rev)
            
            maes[name].append(mae_val)
            mses[name].append(mse_val)
            rmses[name].append(rmse_val)
            r2s[name].append(r2_val)
        
        unit = "Raw COGS" if is_cogs else "Value"
        print(f"  Prophet   | MAE: {maes['prophet'][-1]:.4f} | RMSE: {rmses['prophet'][-1]:.4f} | R2: {r2s['prophet'][-1]:.4f} ({unit})")
        print(f"    CI % (1-90): {ci_p1[-1]*100:.2f}% | (91-365): {ci_p2[-1]*100:.2f}% | (366-548): {ci_p3[-1]*100:.2f}%")
        print(f"  TimeMixer | MAE: {maes['timemixer'][-1]:.4f} | RMSE: {rmses['timemixer'][-1]:.4f} | R2: {r2s['timemixer'][-1]:.4f} ({unit})")
        print(f"  LGBM      | MAE: {maes['lgbm'][-1]:.4f} | RMSE: {rmses['lgbm'][-1]:.4f} | R2: {r2s['lgbm'][-1]:.4f} ({unit})")
        print(f"  Ensemble  | MAE: {maes['ensemble'][-1]:.4f} | RMSE: {rmses['ensemble'][-1]:.4f} | R2: {r2s['ensemble'][-1]:.4f} ({unit})")
        
    print(f"\n=== CV Summary for {target} (EXP WEIGHTED) ===")
    models = ["prophet", "timemixer", "lgbm", "ensemble"]
    rows = []
    unit_label = "Raw COGS" if is_cogs else target.capitalize()
    
    # Calculate exponential weights e^-i where i is distance from newest
    # newest i=0 -> e^0=1, oldest i=n-1 -> e^-(n-1)
    dists = np.arange(n_splits)[::-1] # [2, 1, 0] for 3 splits
    fold_w = np.exp(-dists)
    fold_w /= fold_w.sum()
    
    for m in models:
        print(f"Model: {m.capitalize()} ({unit_label})")
        for i in range(n_splits):
            print(f"  Fold {i} MAE: {maes[m][i]:.4f} | RMSE: {rmses[m][i]:.4f} | R2: {r2s[m][i]:.4f} (Weight: {fold_w[i]:.3f})")
            row = {
                "target": target, "model": m, "fold": i, "unit": unit_label,
                "mae": maes[m][i], "mse": mses[m][i], "rmse": rmses[m][i], "r2": r2s[m][i],
                "fold_weight": fold_w[i]
            }
            if m in ("prophet", "ensemble"):
                row.update({"ci_1_90": ci_p1[i], "ci_91_365": ci_p2[i], "ci_366_548": ci_p3[i]})
            rows.append(row)
            
        m_mae = np.sum(np.array(maes[m]) * fold_w)
        m_mse = np.sum(np.array(mses[m]) * fold_w)
        m_rmse = np.sum(np.array(rmses[m]) * fold_w)
        m_r2 = np.sum(np.array(r2s[m]) * fold_w)
        
        print(f"  EXP WT MEAN | MAE: {m_mae:.4f} | RMSE: {m_rmse:.4f} | R2: {m_r2:.4f}")
        if m in ("prophet", "ensemble"):
            m_p1 = np.sum(np.array(ci_p1) * fold_w)
            m_p2 = np.sum(np.array(ci_p2) * fold_w)
            m_p3 = np.sum(np.array(ci_p3) * fold_w)
            print(f"  EXP WT CI % | (1-90): {m_p1*100:.2f}% | (91-365): {m_p2*100:.2f}% | (366-548): {m_p3*100:.2f}%")
        print("")
        
        row_mean = {
            "target": target, "model": m, "fold": "EXP_WT_MEAN", "unit": unit_label,
            "mae": m_mae, "mse": m_mse, "rmse": m_rmse, "r2": m_r2
        }
        if m in ("prophet", "ensemble"):
            row_mean.update({"ci_1_90": m_p1, "ci_91_365": m_p2, "ci_366_548": m_p3})
        rows.append(row_mean)
    
    cv_res_df = pd.DataFrame(rows)
    out_path = ARTIFACT_DIR / f"cv_results_{target}.csv"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    cv_res_df.to_csv(out_path, index=False)
    print(f"Saved CV results to {out_path}")
    print("-" * 40)


def _predict_future(df: pd.DataFrame, target: str, lgb_cfg: dict, tm_cfg: dict) -> pd.DataFrame:
    fut = pd.read_csv(FEATURE_DIR / "temporal_xreg_future.csv", parse_dates=["ds"])
    prophet_fc = _predict_prophet(df, fut["ds"])
    tm_f = _predict_timemixer(df, tm_cfg, target)
    lgb_f = _predict_lgb_ensemble(df, fut, lgb_cfg, target)
    
    res = pd.DataFrame({"ds": fut["ds"]})
    res["prophet"] = prophet_fc["yhat"].values
    res["prophet_lower"] = prophet_fc["yhat_lower"].values
    res["prophet_upper"] = prophet_fc["yhat_upper"].values
    res["timemixer"] = tm_f
    res["lgbm"] = lgb_f
    return res


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
        lgb_cfg = _load_json(ARTIFACT_DIR / "best_configs" / f"lgb_ensemble_{target}.json")
        tm_cfg = _load_json(ARTIFACT_DIR / "best_configs" / f"timemixer_{target}.json")

        all_cfg = {"lgbm": lgb_cfg, "timemixer": tm_cfg}

        s = args.w_prophet + args.w_timemixer + args.w_lgbm
        w = np.array([args.w_prophet, args.w_timemixer, args.w_lgbm], dtype=float) / s
        
        evaluate_cv(df, target, all_cfg, w, n_splits=3, step=365, horizon=548)

        base_future = _predict_future(df, target, lgb_cfg, tm_cfg)

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
