"""Backtest metric calculations."""
from __future__ import annotations

from typing import Dict, List


def compute_metrics(trades: List[Dict[str, float]]) -> Dict[str, float]:
    """Compute summary metrics from trade results."""
    total = len(trades)
    if total == 0:
        return {"trades": 0, "win_rate": 0.0, "expectancy": 0.0, "max_drawdown": 0.0}

    wins = [trade for trade in trades if trade.get("pnl", 0.0) > 0]
    win_rate = len(wins) / total

    r_multiples = [trade.get("r_multiple", 0.0) for trade in trades]
    expectancy = sum(r_multiples) / total

    equity = 0.0
    max_equity = 0.0
    max_drawdown = 0.0
    for trade in trades:
        equity += trade.get("pnl", 0.0)
        max_equity = max(max_equity, equity)
        max_drawdown = max(max_drawdown, max_equity - equity)

    return {
        "trades": total,
        "win_rate": win_rate,
        "expectancy": expectancy,
        "max_drawdown": max_drawdown,
    }
