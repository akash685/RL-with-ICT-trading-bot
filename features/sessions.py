"""Session encoding utilities."""
from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict

if TYPE_CHECKING:
    import pandas as pd


def encode_sessions(data: "pd.DataFrame", config: Dict[str, Any]) -> "pd.DataFrame":
    """Encode time-based trading sessions (London/NY kill zones).

    Args:
        data: OHLCV dataframe with timestamps.
        config: Configuration options (session windows).

    Returns:
        Dataframe with session encoding columns appended.
    """
    data = data.copy()
    data["session_london"] = 0
    data["session_ny"] = 0
    data["session_lunch"] = 0
    return data
