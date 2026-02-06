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

    impulse_threshold = float(config.get("order_block_impulse", 0.0))
    body = (data["close"] - data["open"]).abs()
    bullish_impulse = (data["close"] > data["open"]) & (body >= impulse_threshold)
    bearish_impulse = (data["close"] < data["open"]) & (body >= impulse_threshold)

    prev_candle = data.shift(1)
    bullish_ob = bullish_impulse & (prev_candle["close"] < prev_candle["open"])
    bearish_ob = bearish_impulse & (prev_candle["close"] > prev_candle["open"])

    data.loc[bullish_ob, "order_block_type"] = "bullish"
    data.loc[bullish_ob, "order_block_high"] = prev_candle.loc[bullish_ob, "high"]
    data.loc[bullish_ob, "order_block_low"] = prev_candle.loc[bullish_ob, "low"]

    data.loc[bearish_ob, "order_block_type"] = "bearish"
    data.loc[bearish_ob, "order_block_high"] = prev_candle.loc[bearish_ob, "high"]
    data.loc[bearish_ob, "order_block_low"] = prev_candle.loc[bearish_ob, "low"]
    return data
