"""Action space definitions for the RL agent."""
from __future__ import annotations

from enum import Enum


class Action(Enum):
    """Discrete trading actions."""

    HOLD = 0
    BUY = 1
    SELL = 2
    CLOSE = 3
