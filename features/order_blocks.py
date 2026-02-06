"""Order block identification."""
from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict

if TYPE_CHECKING:
    import pandas as pd


def compute_order_blocks(data: "pd.DataFrame", config: Dict[str, Any]) -> "pd.DataFrame":
    """Identify bullish/bearish order blocks.

    Args:
        data: OHLCV dataframe.
        config: Configuration options (impulse threshold, lookback).

    Returns:
        Dataframe with order block metadata appended.
    """
    data = data.copy()
    data["order_block_type"] = None
    data["order_block_high"] = None
    data["order_block_low"] = None
    return data
