"""Fair value gap (FVG) detection."""
from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict

if TYPE_CHECKING:
    import pandas as pd


def compute_fair_value_gaps(data: "pd.DataFrame", config: Dict[str, Any]) -> "pd.DataFrame":
    """Detect FVG zones and mark fills.

    Args:
        data: OHLCV dataframe.
        config: Configuration options (gap size threshold).

    Returns:
        Dataframe with FVG columns appended.
    """
    data = data.copy()
    data["fvg_direction"] = None
    data["fvg_filled"] = False
    data["fvg_size"] = 0.0

    gap_threshold = float(config.get("fvg_min_gap", 0.0))
    prev_high = data["high"].shift(1)
    next_low = data["low"].shift(-1)
    prev_low = data["low"].shift(1)
    next_high = data["high"].shift(-1)

    bullish_gap = prev_high < next_low - gap_threshold
    bearish_gap = prev_low > next_high + gap_threshold

    data.loc[bullish_gap, "fvg_direction"] = "bullish"
    data.loc[bearish_gap, "fvg_direction"] = "bearish"
    data.loc[bullish_gap, "fvg_size"] = (next_low - prev_high).abs()
    data.loc[bearish_gap, "fvg_size"] = (prev_low - next_high).abs()

    data["fvg_filled"] = False
    return data
