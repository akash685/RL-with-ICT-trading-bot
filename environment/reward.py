"""Reward function utilities."""
from __future__ import annotations

from typing import Dict


def calculate_reward(trade_result: Dict[str, float]) -> float:
    """Compute reward from trade results in R-multiples.

    Args:
        trade_result: Dictionary with keys like "r_multiple" or "drawdown".

    Returns:
        Calculated reward.
    """
    r_multiple = trade_result.get("r_multiple", 0.0)
    overtrade_penalty = trade_result.get("overtrade_penalty", 0.0)
    drawdown_penalty = trade_result.get("drawdown_penalty", 0.0)
    holding_penalty = trade_result.get("holding_penalty", 0.0)
    return r_multiple - overtrade_penalty - drawdown_penalty - holding_penalty
