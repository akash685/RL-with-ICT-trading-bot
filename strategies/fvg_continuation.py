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
    signals["signal"] = 0
    signals["signal_reason"] = ""
    return signals
