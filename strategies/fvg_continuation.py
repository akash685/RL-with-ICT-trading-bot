"""FVG continuation strategy."""
from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict

if TYPE_CHECKING:
    import pandas as pd


def generate_fvg_continuation_signals(features: "pd.DataFrame", config: Dict[str, Any]) -> "pd.DataFrame":
    """Generate trade signals for the FVG continuation setup.

    Args:
        features: Feature dataframe with FVG and trend signals.
        config: Strategy configuration.

    Returns:
        Dataframe with signal columns appended.
    """
    signals = features.copy()
    defaults = {
        "fvg_direction": None,
        "fvg_filled": False,
        "structure_direction": "neutral",
        "bos": False,
        "mss": False,
    }
    for column, default in defaults.items():
        if column not in signals.columns:
            signals[column] = default

    trend_source = config.get("fvg_trend_source", "structure_direction")
    if trend_source not in signals.columns:
        trend_source = "structure_direction"

    if trend_source == "bos":
        trend_bullish = signals["bos"]
        trend_bearish = signals["mss"]
    else:
        trend_bullish = signals[trend_source] == "bullish"
        trend_bearish = signals[trend_source] == "bearish"

    signals["signal"] = 0
    signals["signal_reason"] = ""

    buy_mask = (
        trend_bullish
        & (signals["fvg_direction"] == "bullish")
        & (~signals["fvg_filled"])
    )
    sell_mask = (
        trend_bearish
        & (signals["fvg_direction"] == "bearish")
        & (~signals["fvg_filled"])
    )

    signals.loc[buy_mask, "signal"] = 1
    signals.loc[buy_mask, "signal_reason"] = "fvg_continuation_long"
    signals.loc[sell_mask, "signal"] = -1
    signals.loc[sell_mask, "signal_reason"] = "fvg_continuation_short"
    return signals
