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
    penalty = trade_result.get("overtrade_penalty", 0.0)
    return r_multiple - penalty
