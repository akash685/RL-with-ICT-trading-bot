"""Build a BTCUSD multi-timeframe feature set and execute a simple trade model."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict

import numpy as np
import pandas as pd

from features import (
    compute_fair_value_gaps,
    compute_indicators,
    compute_liquidity,
    compute_market_structure,
    compute_order_blocks,
    compute_premium_discount,
    compute_smt_divergence,
    encode_sessions,
)

TIMEFRAMES = {
    "1w": "1W",
    "1d": "1D",
    "4hr": "4h",
    "2hr": "2h",
    "1hr": "1h",
    "30min": "30min",
    "15min": "15min",
    "5min": "5min",
}


def load_btcusd_5min(source_csv: str | None = None) -> pd.DataFrame:
    """Load BTCUSD 5-minute OHLCV data."""
    source = source_csv or "data/btcusd_5min_sample.csv"
    df = pd.read_csv(source)
    required = {"timestamp", "open", "high", "low", "close", "volume"}
    missing = required.difference(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    out = (
        df.assign(timestamp=lambda x: pd.to_datetime(x["timestamp"], utc=True, errors="coerce"))
        .dropna(subset=["timestamp"])
        .sort_values("timestamp")
        .drop_duplicates(subset=["timestamp"])
        .reset_index(drop=True)
    )
    if len(out) < 1000:
        raise ValueError("Need at least 1000 rows of 5-minute BTCUSD data.")
    return out


def resample_ohlcv(df_5m: pd.DataFrame, rule: str) -> pd.DataFrame:
    """Resample 5-minute OHLCV to a higher timeframe."""
    rs = (
        df_5m.set_index("timestamp")
        .resample(rule)
        .agg({
            "open": "first",
            "high": "max",
            "low": "min",
            "close": "last",
            "volume": "sum",
        })
        .dropna()
        .reset_index()
    )
    return rs


def build_features(df: pd.DataFrame, config: Dict[str, Any]) -> pd.DataFrame:
    """Apply the same feature stack to one timeframe dataframe."""
    feat = df.rename(
        columns={"open": "Open", "high": "High", "low": "Low", "close": "Close", "volume": "Volume"}
    ).copy()
    feat.columns = [c.lower() if c != "timestamp" else c for c in feat.columns]

    feat = compute_market_structure(feat, config)
    feat = compute_liquidity(feat, config)
    feat = compute_order_blocks(feat, config)
    feat = compute_fair_value_gaps(feat, config)
    feat = compute_premium_discount(feat, config)
    feat = encode_sessions(feat, config)
    feat = compute_smt_divergence(feat, config)
    feat = compute_indicators(feat, config)

    feat["tf_signal"] = 0
    feat.loc[(feat["bos"] == True) & (feat["fvg_direction"] == "bullish"), "tf_signal"] = 1
    feat.loc[(feat["mss"] == True) & (feat["fvg_direction"] == "bearish"), "tf_signal"] = -1
    return feat


def merge_timeframes(tf_features: Dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Align all timeframe features onto 5-minute bars using asof merge."""
    base = tf_features["5min"].copy()
    base = base[["timestamp", "close", "tf_signal"]].rename(columns={"tf_signal": "signal_5min", "close": "close_5min"})

    for tf_name, feat in tf_features.items():
        if tf_name == "5min":
            continue
        cols = ["timestamp", "tf_signal", "bos", "mss", "fvg_direction", "volatility", "trend_strength"]
        small = feat[cols].sort_values("timestamp").copy()
        small = small.rename(columns={c: f"{tf_name}_{c}" for c in small.columns if c != "timestamp"})
        base = pd.merge_asof(
            base.sort_values("timestamp"),
            small.sort_values("timestamp"),
            on="timestamp",
            direction="backward",
        )

    signal_cols = ["signal_5min"] + [f"{k}_tf_signal" for k in tf_features.keys() if k != "5min"]
    weight_map = {
        "signal_5min": 1.0,
        "15min_tf_signal": 1.1,
        "30min_tf_signal": 1.2,
        "1hr_tf_signal": 1.4,
        "2hr_tf_signal": 1.6,
        "4hr_tf_signal": 1.8,
        "1d_tf_signal": 2.0,
        "1w_tf_signal": 2.3,
    }
    for c in signal_cols:
        if c not in base.columns:
            base[c] = 0
        base[c] = base[c].fillna(0)

    weighted_sum = np.zeros(len(base), dtype=float)
    for c in signal_cols:
        weighted_sum += base[c].to_numpy() * weight_map.get(c, 1.0)

    base["combined_signal"] = np.where(weighted_sum > 0, 1, np.where(weighted_sum < 0, -1, 0))
    return base


def execute_trade_model(merged: pd.DataFrame) -> Dict[str, float]:
    """Run a simple execution model on merged multi-timeframe signal."""
    close = merged["close_5min"].to_numpy(dtype=float)
    signal = merged["combined_signal"].to_numpy(dtype=float)

    returns = np.zeros_like(close)
    returns[1:] = (close[1:] - close[:-1]) / np.maximum(close[:-1], 1e-9)

    strategy_returns = np.zeros_like(close)
    strategy_returns[1:] = signal[:-1] * returns[1:]

    equity = np.cumprod(1.0 + strategy_returns)
    peak = np.maximum.accumulate(equity)
    drawdown = np.where(peak > 0, (equity - peak) / peak, 0)

    trades = int(np.sum(np.abs(np.diff(signal)) > 0))
    win_rate = float(np.mean(strategy_returns[strategy_returns != 0] > 0)) if np.any(strategy_returns != 0) else 0.0

    return {
        "bars": float(len(merged)),
        "trades": float(trades),
        "total_return_pct": float((equity[-1] - 1.0) * 100),
        "avg_bar_return_pct": float(np.mean(strategy_returns) * 100),
        "win_rate": float(win_rate),
        "max_drawdown_pct": float(np.min(drawdown) * 100),
    }


def run_pipeline(source_csv: str | None, output_features: Path, output_metrics: Path) -> None:
    config: Dict[str, Any] = {}
    df_5m = load_btcusd_5min(source_csv)

    tf_features: Dict[str, pd.DataFrame] = {}
    for name, rule in TIMEFRAMES.items():
        rs = resample_ohlcv(df_5m, rule)
        tf_features[name] = build_features(rs, config)

    merged = merge_timeframes(tf_features)
    metrics = execute_trade_model(merged)

    output_features.parent.mkdir(parents=True, exist_ok=True)
    output_metrics.parent.mkdir(parents=True, exist_ok=True)

    merged.to_csv(output_features, index=False)
    output_metrics.write_text(json.dumps(metrics, indent=2), encoding="utf-8")

    print(f"Saved merged multi-timeframe dataset: {output_features}")
    print(f"Saved execution metrics: {output_metrics}")
    print(json.dumps(metrics, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser(description="Build BTCUSD multi-timeframe features and execute model.")
    parser.add_argument("--source-csv", default=None, help="BTCUSD 5-minute CSV path with timestamp/open/high/low/close/volume")
    parser.add_argument("--output-features", type=Path, default=Path("artifacts/btcusd_mtf_features.csv"))
    parser.add_argument("--output-metrics", type=Path, default=Path("artifacts/btcusd_mtf_metrics.json"))
    args = parser.parse_args()

    run_pipeline(args.source_csv, args.output_features, args.output_metrics)


if __name__ == "__main__":
    main()
