"""Stop loss calculations."""
from __future__ import annotations

from typing import Dict


def calculate_stop_loss(risk_config: Dict[str, float]) -> float:
    """Calculate stop loss distance from risk settings."""
    return risk_config.get("stop_loss", 0.0)
