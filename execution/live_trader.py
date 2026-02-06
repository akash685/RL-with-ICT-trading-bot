"""Live trading loop."""
from __future__ import annotations

from typing import Dict

from .broker_api import BrokerAPI


class LiveTrader:
    """Executes live trades using a broker API."""

    def __init__(self, broker: BrokerAPI, config: Dict[str, str]):
        self.broker = broker
        self.config = config

    def execute(self, order: Dict[str, str]) -> Dict[str, str]:
        """Execute a live order."""
        return self.broker.place_order(order)
