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
    timezone = config.get("session_timezone", "UTC")
    london_window = config.get("london_session", (7, 10))
    ny_window = config.get("ny_session", (13, 16))
    lunch_window = config.get("ny_lunch", (16, 18))

    timestamps = data["timestamp"]
    if not timestamps.dt.tz:
        timestamps = timestamps.dt.tz_localize("UTC")
    timestamps = timestamps.dt.tz_convert(timezone)
    hours = timestamps.dt.hour

    data["session_london"] = ((hours >= london_window[0]) & (hours < london_window[1])).astype(int)
    data["session_ny"] = ((hours >= ny_window[0]) & (hours < ny_window[1])).astype(int)
    data["session_lunch"] = ((hours >= lunch_window[0]) & (hours < lunch_window[1])).astype(int)
    return data
