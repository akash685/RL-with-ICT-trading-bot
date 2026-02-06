"""Backtest metric calculations."""
from __future__ import annotations

from typing import Dict, List


def compute_metrics(trades: List[Dict[str, float]]) -> Dict[str, float]:
    """Compute summary metrics from trade results."""
    total = len(trades)
    return {"trades": total, "win_rate": 0.0, "expectancy": 0.0, "max_drawdown": 0.0}
