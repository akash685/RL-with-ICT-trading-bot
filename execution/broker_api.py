"""Broker API abstraction."""
from __future__ import annotations

from typing import Dict


class BrokerAPI:
    """Placeholder broker API client."""

    def __init__(self, config: Dict[str, str]):
        self.config = config

    def place_order(self, order: Dict[str, str]) -> Dict[str, str]:
        """Submit an order to the broker."""
        return {"status": "submitted", "order_id": "demo"}
