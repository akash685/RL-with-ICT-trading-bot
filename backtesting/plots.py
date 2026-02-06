"""Plotting utilities for backtests."""
from __future__ import annotations

from typing import Dict, List


def prepare_equity_curve(trades: List[Dict[str, float]]) -> List[float]:
    """Return an equity curve series for plotting."""
    return [0.0]
