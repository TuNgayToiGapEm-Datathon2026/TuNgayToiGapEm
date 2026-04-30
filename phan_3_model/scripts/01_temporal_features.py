"""
01_temporal_features.py — Temporal-only feature engineering.

Builds only future-safe temporal features (calendar/fourier/tet/holiday)
plus fixed promotion-schedule features, then writes:

  data/features/temporal_xreg_train.csv
  data/features/temporal_xreg_future.csv
  data/processed/revenue_temporal.csv
  data/processed/cogs_ratio_temporal.csv
"""

import calendar
import sys
import time
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd
import yaml

# ═══════════════════════════════════════════════════════════════════════════════
# Constants & Constants from src/features.py
# ═══════════════════════════════════════════════════════════════════════════════

TET_DATES: dict[int, str] = {
    2012: "2012-01-23", 2013: "2013-02-10", 2014: "2014-01-31", 2015: "2015-02-19",
    2016: "2016-02-08", 2017: "2017-01-28", 2018: "2018-02-16", 2019: "2019-02-05",
    2020: "2020-01-25", 2021: "2021-02-12", 2022: "2022-02-01", 2023: "2023-01-22",
    2024: "2024-02-10",
}

HUNG_KINGS_DATES: dict[int, str] = {
    2012: "2012-03-31", 2013: "2013-04-19", 2014: "2014-04-09", 2015: "2015-04-28",
    2016: "2016-04-16", 2017: "2017-04-06", 2018: "2018-04-25", 2019: "2019-04-14",
    2020: "2020-04-02", 2021: "2021-04-21", 2022: "2022-04-10", 2023: "2023-04-29",
    2024: "2024-04-18",
}

# (name, month_start, day_start, duration_days, promo_strength, year_flag)
PROMO_SCHEDULE = [
    ("spring_sale", 3, 18, 30, 12, True),
    ("mid_year", 6, 23, 29, 18, True),
    ("fall_launch", 8, 30, 32, 10, True),
    ("year_end", 11, 18, 45, 20, True),
    ("urban_blowout", 7, 30, 33, None, "odd"),
    ("rural_special", 1, 30, 30, 15, "odd"),
]

@dataclass
class PromoWindow:
    name: str
    start: pd.Timestamp
    end: pd.Timestamp
    strength: float

# ═══════════════════════════════════════════════════════════════════════════════
# Loader functions from src/loader.py
# ═══════════════════════════════════════════════════════════════════════════════

def load_raw(raw_dir: str | Path = "data/raw") -> pd.DataFrame:
    raw_dir = Path(raw_dir)
    sales = pd.read_csv(raw_dir / "sales.csv", parse_dates=["Date"])
    revenue = pd.DataFrame({"unique_id": "revenue", "ds": sales["Date"], "y": sales["Revenue"]})
    cogs_ratio = pd.DataFrame({"unique_id": "cogs_ratio", "ds": sales["Date"], "y": sales["COGS"] / sales["Revenue"]})
    df = pd.concat([revenue, cogs_ratio], ignore_index=True)
    df["ds"] = pd.to_datetime(df["ds"])
    return df

def prepare_train_test_split(df: pd.DataFrame, test_start: str = "2023-01-01") -> tuple[pd.DataFrame, pd.DataFrame]:
    test_start_dt = pd.Timestamp(test_start)
    train_df = df.loc[df["ds"] < test_start_dt].copy().reset_index(drop=True)
    horizon_dates = pd.date_range(start=test_start, periods=548, freq="D")
    unique_ids = df["unique_id"].unique()
    test_horizon = pd.DataFrame({
        "unique_id": [uid for uid in unique_ids for _ in horizon_dates],
        "ds": list(horizon_dates) * len(unique_ids),
        "y": float("nan"),
    })
    return train_df, test_horizon

# ═══════════════════════════════════════════════════════════════════════════════
# Feature builders from src/features.py
# ═══════════════════════════════════════════════════════════════════════════════

def build_calendar_features(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    ds = pd.to_datetime(out["ds"])
    out["day_of_week"] = ds.dt.dayofweek
    out["day_of_month"] = ds.dt.day
    out["day_of_year"] = ds.dt.dayofyear
    out['days_to_eom']   = ds.dt.days_in_month - out['day_of_month']
    out['days_from_som'] = out['day_of_month'] - 1
    out["month"] = ds.dt.month
    out["quarter"] = ds.dt.quarter
    out["year"] = ds.dt.year
    out["is_weekend"] = ds.dt.dayofweek.isin([5, 6]).astype(int)
    out['regime_pre2019']  = (out['year']<=2018).astype(int)
    out['regime_2019']     = (out['year']==2019).astype(int)
    out['regime_post2019'] = (out['year']>=2020).astype(int)
    out["is_odd_year"] = (ds.dt.year % 2 != 0).astype(int)
    out["is_first3"] = (ds.dt.day <= 3).astype(int)
    out["is_last5"] = (ds.dt.days_in_month - ds.dt.day < 5).astype(int)
    return out

def build_fourier_features(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    ds = pd.to_datetime(out["ds"])
    t = (ds - pd.Timestamp("2012-01-01")).dt.days
    for k in range(1, 6):
        out[f"fourier_ann_sin_{k}"] = np.sin(2 * np.pi * k * t / 365.25)
        out[f"fourier_ann_cos_{k}"] = np.cos(2 * np.pi * k * t / 365.25)
    for k in range(1, 3):
        out[f"fourier_week_sin_{k}"] = np.sin(2 * np.pi * k * t / 7.0)
        out[f"fourier_week_cos_{k}"] = np.cos(2 * np.pi * k * t / 7.0)
    for k in range(1, 3):
        out[f"fourier_month_sin_{k}"] = np.sin(2 * np.pi * k * t / 30.44)
        out[f"fourier_month_cos_{k}"] = np.cos(2 * np.pi * k * t / 30.44)
    return out

def build_tet_features(df: pd.DataFrame, window: int = 21) -> pd.DataFrame:
    out = df.copy()
    ds = pd.to_datetime(out["ds"])
    tet_ts = sorted(pd.Timestamp(d) for d in TET_DATES.values())
    is_tet_period = np.zeros(len(ds), dtype=int)
    days_until_tet = np.full(len(ds), -1, dtype=int)
    days_since_tet = np.full(len(ds), -1, dtype=int)
    for i, d in enumerate(ds):
        d = pd.Timestamp(d)
        past = [t for t in tet_ts if t <= d]
        future = [t for t in tet_ts if t > d]
        if past:
            diff_since = (d - past[-1]).days
            if 0 <= diff_since <= window: days_since_tet[i] = diff_since
        if future:
            diff_until = (future[0] - d).days
            if 0 <= diff_until <= window: days_until_tet[i] = diff_until
        if days_since_tet[i] != -1 or days_until_tet[i] != -1 or d in tet_ts:
            is_tet_period[i] = 1
    out["is_tet_period"] = is_tet_period
    out["days_until_tet"] = days_until_tet
    out["days_since_tet"] = days_since_tet
    return out

def build_holiday_features(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    ds = pd.to_datetime(out["ds"])
    is_holiday = (((ds.dt.month == 11) & (ds.dt.day == 11)) | ((ds.dt.month == 12) & (ds.dt.day == 12)))
    for year in ds.dt.year.unique():
        nov_fridays = pd.date_range(start=f"{year}-11-01", end=f"{year}-11-30", freq="W-FRI")
        if len(nov_fridays) >= 4: is_holiday |= (ds == nov_fridays[3])
    is_holiday |= (((ds.dt.month == 3) & (ds.dt.day == 8)) | ((ds.dt.month == 10) & (ds.dt.day == 20)) |
                   ((ds.dt.month == 12) & (ds.dt.day == 24)) | ((ds.dt.month == 12) & (ds.dt.day == 25)))
    holidays_set = set()
    for year in ds.dt.year.unique():
        year = int(year)
        holidays_set.add(pd.Timestamp(f"{year}-01-01"))
        holidays_set.add(pd.Timestamp(f"{year}-04-30"))
        holidays_set.add(pd.Timestamp(f"{year}-05-01"))
        holidays_set.add(pd.Timestamp(f"{year}-09-02"))
        if year in HUNG_KINGS_DATES: holidays_set.add(pd.Timestamp(HUNG_KINGS_DATES[year]))
        if year in TET_DATES:
            tet = pd.Timestamp(TET_DATES[year])
            for offset in range(-1, 4): holidays_set.add(tet + pd.Timedelta(days=offset))
    is_holiday |= ds.isin(holidays_set)
    out["is_holiday"] = is_holiday.astype(int)
    return out

# ═══════════════════════════════════════════════════════════════════════════════
# Internal Helper functions
# ═══════════════════════════════════════════════════════════════════════════════

def _safe_date(year: int, month: int, day: int) -> pd.Timestamp:
    last_day = calendar.monthrange(year, month)[1]
    return pd.Timestamp(year=year, month=month, day=min(day, last_day))

def _year_allowed(year: int, flag) -> bool:
    if flag is True: return True
    if isinstance(flag, str) and flag.lower() == "odd": return year % 2 == 1
    return False

def _expand_schedule(dates: pd.Series) -> list[PromoWindow]:
    years = sorted(pd.to_datetime(dates).dt.year.unique())
    years = list(range(min(years) - 1, max(years) + 2))
    windows: list[PromoWindow] = []
    for year in years:
        for name, month_start, day_start, duration_days, promo_strength, year_flag in PROMO_SCHEDULE:
            if not _year_allowed(year, year_flag): continue
            start = _safe_date(year, int(month_start), int(day_start))
            end = start + pd.Timedelta(days=int(duration_days) - 1)
            strength = float(promo_strength) if promo_strength is not None else 0.0
            windows.append(PromoWindow(name=name, start=start, end=end, strength=strength))
    return windows

def build_fixed_promo_features(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    ds = pd.to_datetime(out["ds"])
    d = pd.Series(ds.values, index=out.index)
    yrs = sorted(set(out["year"].tolist()))
    for name, sm, sd, dur, disc, recur in PROMO_SCHEDULE:
        in_prom = np.zeros(len(out), dtype=int)
        since = np.full(len(out), -1.0)
        until = np.full(len(out), -1.0)
        discount = np.zeros(len(out), dtype=float)
        for y in range(min(yrs) - 1, max(yrs) + 2):
            if recur == "odd" and y % 2 == 0: continue
            start = _safe_date(y, int(sm), int(sd))
            end = start + pd.Timedelta(days=int(dur) - 1)
            mask = (d >= start) & (d <= end)
            in_prom[mask] = 1
            since[mask] = (d[mask] - start).dt.days.astype(float)
            until[mask] = (end - d[mask]).dt.days.astype(float)
            discount[mask] = float(disc or 0.0)
        out[f"promo_{name}"] = in_prom
        out[f"promo_{name}_since"] = since
        out[f"promo_{name}_until"] = until
        out[f"promo_{name}_disc"] = discount
    return out

def build_temporal_only(dates, unique_id: str = "total") -> pd.DataFrame:
    feat = pd.DataFrame({"unique_id": unique_id, "ds": pd.to_datetime(dates)})
    feat = build_calendar_features(feat)
    feat = build_fourier_features(feat)
    feat = build_tet_features(feat)
    feat = build_holiday_features(feat)
    feat = build_fixed_promo_features(feat)
    return feat

def main() -> None:
    t0 = time.time()
    PROJECT_ROOT = Path(__file__).resolve().parent.parent
    cfg = yaml.safe_load(open(PROJECT_ROOT / "config" / "general.yaml", "r", encoding="utf-8"))
    raw_dir = PROJECT_ROOT / cfg["raw_dir"]
    processed_dir = PROJECT_ROOT / cfg["processed_dir"]
    features_dir = PROJECT_ROOT / cfg["features_dir"]
    processed_dir.mkdir(parents=True, exist_ok=True)
    features_dir.mkdir(parents=True, exist_ok=True)

    print("[1/4] Loading raw sales ...")
    df = load_raw(raw_dir)

    print(f"[2/4] Splitting at {cfg['test_start']} ...")
    train_df, _ = prepare_train_test_split(df, test_start=cfg["test_start"])

    print("[3/4] Building temporal-only train features ...")
    train_dates = train_df["ds"].drop_duplicates().sort_values().reset_index(drop=True)
    temporal_train = build_temporal_only(train_dates)
    temporal_train.to_csv(features_dir / "temporal_xreg_train.csv", index=False)

    print("[4/4] Building temporal-only future features ...")
    future_dates = pd.date_range(start=cfg["test_start"], periods=int(cfg["horizon"]), freq="D")
    temporal_future = build_temporal_only(future_dates)
    temporal_future.to_csv(features_dir / "temporal_xreg_future.csv", index=False)

    temporal_cols = [c for c in temporal_train.columns if c not in {"unique_id", "ds"}]
    rev = train_df[train_df["unique_id"] == "revenue"][["unique_id", "ds", "y"]].copy()
    cogs = train_df[train_df["unique_id"] == "cogs_ratio"][["unique_id", "ds", "y"]].copy()
    rev = rev.merge(temporal_train[["ds"] + temporal_cols], on="ds", how="left")
    cogs = cogs.merge(temporal_train[["ds"] + temporal_cols], on="ds", how="left")
    rev.to_csv(processed_dir / "revenue_temporal.csv", index=False)
    cogs.to_csv(processed_dir / "cogs_ratio_temporal.csv", index=False)

    print(f"      -> {features_dir / 'temporal_xreg_train.csv'}")
    print(f"      -> {features_dir / 'temporal_xreg_future.csv'}")
    print(f"      -> {processed_dir / 'revenue_temporal.csv'}")
    print(f"      -> {processed_dir / 'cogs_ratio_temporal.csv'}")
    print(f"\nDone in {time.time() - t0:.1f}s")

if __name__ == "__main__":
    main()
