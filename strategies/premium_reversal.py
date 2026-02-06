"""Premium/discount reversal strategy."""
from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict

if TYPE_CHECKING:
    import pandas as pd


def generate_premium_reversal_signals(features: "pd.DataFrame", config: Dict[str, Any]) -> "pd.DataFrame":
    """Generate trade signals for premium/discount reversals.

    Args:
        features: Feature dataframe with liquidity and premium/discount zones.
        config: Strategy configuration.

    Returns:
        Dataframe with signal columns appended.
    """
    signals = features.copy()
    defaults = {
        "premium_discount_zone": "equilibrium",
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
        (signals["premium_discount_zone"] == "discount")
        & signals["liquidity_sweep"]
        & signals["mss"]
        & (signals["order_block_type"] == "bullish")
    )
    sell_mask = (
        (signals["premium_discount_zone"] == "premium")
        & signals["liquidity_sweep"]
        & signals["mss"]
        & (signals["order_block_type"] == "bearish")
    )

    signals.loc[buy_mask, "signal"] = 1
    signals.loc[buy_mask, "signal_reason"] = "premium_reversal_long"
    signals.loc[sell_mask, "signal"] = -1
    signals.loc[sell_mask, "signal_reason"] = "premium_reversal_short"
    return signals
