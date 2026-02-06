"""Additional indicator calculations."""
from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict

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
    data["volatility"] = 0.0
    data["trend_strength"] = 0.0
    return data
