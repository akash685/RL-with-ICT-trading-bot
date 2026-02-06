"""Premium/discount zone calculations."""
from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict

if TYPE_CHECKING:
    import pandas as pd


def compute_premium_discount(data: "pd.DataFrame", config: Dict[str, Any]) -> "pd.DataFrame":
    """Compute premium/discount zones from recent swing highs/lows.

    Args:
        data: OHLCV dataframe.
        config: Configuration options (swing window).

    Returns:
        Dataframe with premium/discount columns appended.
    """
    data = data.copy()
    lookback = int(config.get("swing_lookback", 20))
    if lookback < 2:
        lookback = 2

    swing_high = data["high"].rolling(window=lookback, min_periods=lookback).max()
    swing_low = data["low"].rolling(window=lookback, min_periods=lookback).min()
    equilibrium = (swing_high + swing_low) / 2.0

    data["equilibrium_price"] = equilibrium
    data["equilibrium_distance"] = data["close"] - equilibrium
    data["premium_discount_zone"] = "equilibrium"
    data.loc[data["close"] > equilibrium, "premium_discount_zone"] = "premium"
    data.loc[data["close"] < equilibrium, "premium_discount_zone"] = "discount"
    return data
