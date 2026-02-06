"""Backtest engine skeleton."""
from __future__ import annotations

from typing import Any, Dict, List


def run_backtest(signals: List[Dict[str, Any]], prices: List[Dict[str, Any]], config: Dict[str, Any]) -> Dict[str, float]:
    """Run a simple backtest loop.

    Args:
        signals: List of signal dicts.
        prices: List of price dicts.
        config: Backtest configuration.

    Returns:
        Summary metrics.
    """
    return {"trades": 0, "win_rate": 0.0, "expectancy": 0.0, "max_drawdown": 0.0}
