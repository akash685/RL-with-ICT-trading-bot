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
    signals["signal"] = 0
    signals["signal_reason"] = ""
    return signals
