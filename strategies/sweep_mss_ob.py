"""Liquidity sweep + MSS + OB entry strategy."""
from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict

if TYPE_CHECKING:
    import pandas as pd


def generate_sweep_mss_ob_signals(features: "pd.DataFrame", config: Dict[str, Any]) -> "pd.DataFrame":
    """Generate trade signals for the sweep/MSS/OB setup.

    Args:
        features: Feature dataframe with liquidity and structure signals.
        config: Strategy configuration.

    Returns:
        Dataframe with signal columns appended.
    """
    signals = features.copy()
    defaults = {
        "liquidity_sweep": False,
        "mss": False,
        "order_block_type": None,
    }
    for column, default in defaults.items():
        if column not in signals.columns:
            signals[column] = default

    signals["signal"] = 0
    signals["signal_reason"] = ""

    buy_mask = (
        signals["liquidity_sweep"]
        & signals["mss"]
        & (signals["order_block_type"] == "bullish")
    )
    sell_mask = (
        signals["liquidity_sweep"]
        & signals["mss"]
        & (signals["order_block_type"] == "bearish")
    )

    signals.loc[buy_mask, "signal"] = 1
    signals.loc[buy_mask, "signal_reason"] = "sweep_mss_ob_long"
    signals.loc[sell_mask, "signal"] = -1
    signals.loc[sell_mask, "signal_reason"] = "sweep_mss_ob_short"
    return signals
