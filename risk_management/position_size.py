"""Position sizing utilities."""
from __future__ import annotations

from typing import Dict


def calculate_position_size(risk_config: Dict[str, float]) -> float:
    """Calculate position size based on account risk settings."""
    account_balance = risk_config.get("account_balance", 0.0)
    risk_percent = risk_config.get("risk_percent", 0.0)
    return account_balance * risk_percent
