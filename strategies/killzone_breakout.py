"""Kill zone momentum strategy."""
from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict

if TYPE_CHECKING:
    import pandas as pd


def generate_killzone_breakout_signals(features: "pd.DataFrame", config: Dict[str, Any]) -> "pd.DataFrame":
    """Generate trade signals for kill zone momentum.

    Args:
        features: Feature dataframe with session encodings.
        config: Strategy configuration.

    Returns:
        Dataframe with signal columns appended.
    """
    signals = features.copy()
    defaults = {
        "session_london": 0,
        "session_ny": 0,
        "session_lunch": 0,
        "volatility": 0.0,
        "structure_direction": "neutral",
        "fvg_direction": None,
    }
    for column, default in defaults.items():
        if column not in signals.columns:
            signals[column] = default

    include_lunch = bool(config.get("include_lunch", True))
    volatility_threshold = float(config.get("killzone_volatility_threshold", 0.0))

    session_active = (signals["session_london"] == 1) | (signals["session_ny"] == 1)
    if include_lunch:
        session_active = session_active | (signals["session_lunch"] == 1)

    volatility_ok = signals["volatility"] >= volatility_threshold
    trend_bullish = signals["structure_direction"] == "bullish"
    trend_bearish = signals["structure_direction"] == "bearish"

    signals["signal"] = 0
    signals["signal_reason"] = ""

    buy_mask = (
        session_active
        & volatility_ok
        & trend_bullish
        & (signals["fvg_direction"] == "bullish")
    )
    sell_mask = (
        session_active
        & volatility_ok
        & trend_bearish
        & (signals["fvg_direction"] == "bearish")
    )

    signals.loc[buy_mask, "signal"] = 1
    signals.loc[buy_mask, "signal_reason"] = "killzone_breakout_long"
    signals.loc[sell_mask, "signal"] = -1
    signals.loc[sell_mask, "signal_reason"] = "killzone_breakout_short"
    return signals
