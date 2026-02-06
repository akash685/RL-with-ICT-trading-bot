"""Paper trading loop."""
from __future__ import annotations

from typing import Dict


class PaperTrader:
    """Simulated trading without broker integration."""

    def __init__(self, config: Dict[str, str]):
        self.config = config
        self.orders: list[Dict[str, str]] = []

    def execute(self, order: Dict[str, str]) -> Dict[str, str]:
        """Store a simulated order."""
        self.orders.append(order)
        return {"status": "paper_submitted", "order_id": str(len(self.orders))}
