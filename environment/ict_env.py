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
        if len(observations) < 2:
            raise ValueError("ICTTradingEnv requires at least 2 observations.")

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

        current_obs = self.observations[self._index]
        next_index = min(self._index + 1, len(self.observations) - 1)
        next_obs = self.observations[next_index]

        current_close = float(current_obs[0])
        next_close = float(next_obs[0])
        direction = 0.0
        if next_close > current_close:
            direction = 1.0
        elif next_close < current_close:
            direction = -1.0

        r_multiple = 0.0
        if action == Action.BUY:
            r_multiple = direction
        elif action == Action.SELL:
            r_multiple = -direction
        elif action == Action.CLOSE:
            r_multiple = 0.05

        trade_result = {"r_multiple": r_multiple, "overtrade_penalty": 0.0}
        reward = calculate_reward(trade_result)

        self.trade_log.append(
            {
                "index": float(self._index),
                "action": float(action.value),
                "close": current_close,
                "next_close": next_close,
                "r_multiple": r_multiple,
            }
        )

        self._index = next_index
        if self._index >= len(self.observations) - 1:
            self._done = True

        info = {"r_multiple": trade_result["r_multiple"], "direction": direction}
        return self.observations[self._index], reward, self._done, info
