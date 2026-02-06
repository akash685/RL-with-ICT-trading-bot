"""Max drawdown checks."""
from __future__ import annotations

from typing import Dict


def check_max_drawdown(risk_config: Dict[str, float], current_drawdown: float) -> bool:
    """Return True if current drawdown is within limits."""
    limit = risk_config.get("max_drawdown", 0.0)
    return current_drawdown <= limit
