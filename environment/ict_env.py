"""Minimal ICT trading environment skeleton."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Tuple

from .action_space import Action
from .reward import calculate_reward


@dataclass
class StepResult:
    observation: List[float]
    reward: float
    done: bool
    info: Dict[str, float]


class ICTTradingEnv:
    """A lightweight environment skeleton (gym-compatible by signature)."""

    def __init__(self, observations: List[List[float]], trade_log: List[Dict[str, float]] | None = None):
        self.observations = observations
        self.trade_log = trade_log or []
        self._index = 0
        self._done = False

    def reset(self) -> List[float]:
        self._index = 0
        self._done = False
        return self.observations[self._index]

    def step(self, action: Action) -> Tuple[List[float], float, bool, Dict[str, float]]:
        if self._done:
            return self.observations[self._index], 0.0, True, {"info": 0.0}

        trade_result = {"r_multiple": 0.0, "overtrade_penalty": 0.0}
        reward = calculate_reward(trade_result)

        self._index = min(self._index + 1, len(self.observations) - 1)
        if self._index >= len(self.observations) - 1:
            self._done = True

        info = {"r_multiple": trade_result["r_multiple"]}
        return self.observations[self._index], reward, self._done, info
