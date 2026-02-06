"""Additional indicator calculations."""
from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict

import numpy as np

if TYPE_CHECKING:
    import pandas as pd


def compute_indicators(data: "pd.DataFrame", config: Dict[str, Any]) -> "pd.DataFrame":
    """Compute generic indicators (volatility, trend strength).

    Args:
        data: OHLCV dataframe.
        config: Configuration options for indicators.

    Returns:
        Dataframe with indicator columns appended.
    """
    data = data.copy()
    price_col = config.get("price_col", "close")
    volatility_window = int(config.get("volatility_window", 14))
    trend_fast_window = int(config.get("trend_fast_window", 5))
    trend_slow_window = int(config.get("trend_slow_window", 20))

    if price_col not in data.columns:
        data["volatility"] = np.nan
        data["trend_strength"] = np.nan
        return data

    returns = data[price_col].pct_change()
    data["volatility"] = (
        returns.rolling(window=volatility_window, min_periods=volatility_window).std()
    )

    fast_ma = data[price_col].rolling(window=trend_fast_window, min_periods=trend_fast_window).mean()
    slow_ma = data[price_col].rolling(window=trend_slow_window, min_periods=trend_slow_window).mean()
    data["trend_strength"] = (fast_ma - slow_ma) / slow_ma.replace(0, np.nan)
    return data
