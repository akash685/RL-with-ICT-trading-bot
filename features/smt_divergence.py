"""SMT divergence calculations."""
from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict

import numpy as np

if TYPE_CHECKING:
    import pandas as pd


def compute_smt_divergence(data: "pd.DataFrame", config: Dict[str, Any]) -> "pd.DataFrame":
    """Compute SMT divergence across correlated markets.

    Args:
        data: OHLCV dataframe containing correlation inputs.
        config: Configuration options (pairs, thresholds).

    Returns:
        Dataframe with SMT divergence columns appended.
    """
    data = data.copy()
    primary_high_col = config.get("primary_high_col", "high")
    primary_low_col = config.get("primary_low_col", "low")
    secondary_high_col = config.get("secondary_high_col", "high_secondary")
    secondary_low_col = config.get("secondary_low_col", "low_secondary")
    window = int(config.get("smt_window", 5))
    threshold = float(config.get("smt_threshold", 0.0))

    required_cols = {
        primary_high_col,
        primary_low_col,
        secondary_high_col,
        secondary_low_col,
    }
    if not required_cols.issubset(data.columns):
        data["smt_divergence"] = 0.0
        data["smt_confirmation"] = 0.0
        return data

    rolling_primary_high = (
        data[primary_high_col].rolling(window=window, min_periods=window).max().shift(1)
    )
    rolling_primary_low = (
        data[primary_low_col].rolling(window=window, min_periods=window).min().shift(1)
    )
    rolling_secondary_high = (
        data[secondary_high_col].rolling(window=window, min_periods=window).max().shift(1)
    )
    rolling_secondary_low = (
        data[secondary_low_col].rolling(window=window, min_periods=window).min().shift(1)
    )

    primary_high_break = data[primary_high_col] > (rolling_primary_high + threshold)
    secondary_high_break = data[secondary_high_col] > (rolling_secondary_high + threshold)
    primary_low_break = data[primary_low_col] < (rolling_primary_low - threshold)
    secondary_low_break = data[secondary_low_col] < (rolling_secondary_low - threshold)

    divergence_signal = np.zeros(len(data), dtype=float)
    divergence_signal[(primary_high_break & ~secondary_high_break)] = 1.0
    divergence_signal[(primary_low_break & ~secondary_low_break)] = -1.0
    divergence_signal[(secondary_high_break & ~primary_high_break)] = -1.0
    divergence_signal[(secondary_low_break & ~primary_low_break)] = 1.0

    high_strength = (data[primary_high_col] - rolling_primary_high) - (
        data[secondary_high_col] - rolling_secondary_high
    )
    low_strength = (rolling_primary_low - data[primary_low_col]) - (
        rolling_secondary_low - data[secondary_low_col]
    )

    high_divergence = primary_high_break ^ secondary_high_break
    low_divergence = primary_low_break ^ secondary_low_break
    divergence_magnitude = np.where(
        high_divergence,
        np.abs(high_strength),
        np.where(low_divergence, np.abs(low_strength), 0.0),
    )
    data["smt_divergence"] = divergence_signal * divergence_magnitude

    confirmation = np.zeros(len(data), dtype=float)
    if {"open", "close"}.issubset(data.columns):
        confirmation[(divergence_signal > 0) & (data["close"] > data["open"])] = 1.0
        confirmation[(divergence_signal < 0) & (data["close"] < data["open"])] = 1.0
    data["smt_confirmation"] = confirmation
    return data
