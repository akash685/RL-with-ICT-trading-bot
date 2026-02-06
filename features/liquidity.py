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
    data["buy_side_liquidity"] = False
    data["sell_side_liquidity"] = False
    data["liquidity_sweep"] = False
    return data
