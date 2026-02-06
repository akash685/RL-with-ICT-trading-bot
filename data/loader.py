"""Data loading utilities for RL training."""
from __future__ import annotations

from typing import Any, Dict, Iterable, List

import pandas as pd

from data.validation import validate_ohlcv
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


def load_ohlcv_csv(path: str, timezone: str = "UTC") -> pd.DataFrame:
    """Load OHLCV data from a CSV file."""
    data = pd.read_csv(path)
    if "timestamp" in data.columns:
        data["timestamp"] = pd.to_datetime(data["timestamp"], utc=True)
        data["timestamp"] = data["timestamp"].dt.tz_convert(timezone)

    issues = validate_ohlcv(data)
    if issues["errors"]:
        raise ValueError("; ".join(issues["errors"]))
    return data


def compute_feature_frame(data: pd.DataFrame, config: Dict[str, Any]) -> pd.DataFrame:
    """Compute feature dataframe for RL observations."""
    features = compute_market_structure(data, config)
    features = compute_liquidity(features, config)
    features = compute_order_blocks(features, config)
    features = compute_fair_value_gaps(features, config)
    features = compute_premium_discount(features, config)
    features = encode_sessions(features, config)
    features = compute_smt_divergence(features, config)
    features = compute_indicators(features, config)
    return features


def build_observations(
    features: pd.DataFrame, feature_columns: Iterable[str] | None = None
) -> List[List[float]]:
    """Convert feature dataframe into list observations."""
    if feature_columns:
        columns = list(feature_columns)
    else:
        numeric_cols = features.select_dtypes(include=["number"]).columns
        columns = [col for col in numeric_cols if col != "volume"]

    observations = features[columns].fillna(0.0).astype(float)
    return observations.values.tolist()
