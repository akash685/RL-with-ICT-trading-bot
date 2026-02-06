"""Market structure detection (BOS/MSS)."""
from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict

if TYPE_CHECKING:
    import pandas as pd


def compute_market_structure(data: "pd.DataFrame", config: Dict[str, Any]) -> "pd.DataFrame":
    """Annotate BOS/MSS signals based on swing highs/lows.

    Args:
        data: OHLCV dataframe.
        config: Configuration options (lookback, thresholds).

    Returns:
        Dataframe with market structure columns appended.
    """
    data = data.copy()
    lookback = int(config.get("swing_lookback", 3))
    if lookback < 1:
        lookback = 1

    rolling_high = data["high"].rolling(window=lookback, min_periods=lookback).max()
    rolling_low = data["low"].rolling(window=lookback, min_periods=lookback).min()

    data["swing_high"] = data["high"] >= rolling_high
    data["swing_low"] = data["low"] <= rolling_low

    data["bos"] = data["close"] > rolling_high.shift(1)
    data["mss"] = data["close"] < rolling_low.shift(1)
    data["structure_direction"] = "neutral"
    data.loc[data["bos"], "structure_direction"] = "bullish"
    data.loc[data["mss"], "structure_direction"] = "bearish"
    return data
