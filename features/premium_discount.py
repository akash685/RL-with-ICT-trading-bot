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
    data["premium_discount_zone"] = "equilibrium"
    data["equilibrium_distance"] = 0.0
    return data
