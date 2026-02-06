"""Liquidity detection utilities."""
from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict

if TYPE_CHECKING:
    import pandas as pd


def compute_liquidity(data: "pd.DataFrame", config: Dict[str, Any]) -> "pd.DataFrame":
    """Detect equal highs/lows and sweep events.

    Args:
        data: OHLCV dataframe.
        config: Configuration options (tolerance, lookback).

    Returns:
        Dataframe with liquidity columns appended.
    """
    data = data.copy()
    lookback = int(config.get("liquidity_lookback", 5))
    tolerance = float(config.get("liquidity_tolerance", 0.0))

    rolling_high = data["high"].rolling(window=lookback, min_periods=lookback).max().shift(1)
    rolling_low = data["low"].rolling(window=lookback, min_periods=lookback).min().shift(1)

    data["buy_side_liquidity"] = (data["high"] - rolling_high).abs() <= tolerance
    data["sell_side_liquidity"] = (data["low"] - rolling_low).abs() <= tolerance

    buy_sweep = data["high"] > (rolling_high + tolerance)
    sell_sweep = data["low"] < (rolling_low - tolerance)
    data["liquidity_sweep"] = buy_sweep | sell_sweep
    return data
