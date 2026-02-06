"""Data validation helpers."""
from __future__ import annotations

from typing import Dict, List

import pandas as pd


REQUIRED_COLUMNS = ["timestamp", "open", "high", "low", "close", "volume"]


def validate_ohlcv(data: pd.DataFrame) -> Dict[str, List[str]]:
    """Validate OHLCV data for missing columns and duplicate timestamps.

    Args:
        data: OHLCV dataframe.

    Returns:
        Dictionary of validation errors and warnings.
    """
    issues: Dict[str, List[str]] = {"errors": [], "warnings": []}

    missing = [col for col in REQUIRED_COLUMNS if col not in data.columns]
    if missing:
        issues["errors"].append(f"Missing columns: {', '.join(missing)}")

    if "timestamp" in data.columns and data["timestamp"].duplicated().any():
        issues["warnings"].append("Duplicate timestamps detected.")

    if data.isnull().any().any():
        issues["warnings"].append("Null values detected in OHLCV data.")

    return issues
