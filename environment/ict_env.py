"""Minimal ICT trading environment skeleton."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Tuple

import numpy as np
from gymnasium import Env, spaces

from .action_space import Action
from .reward import calculate_reward


@dataclass
class StepResult:
    observation: List[float]
    reward: float
    done: bool
    info: Dict[str, float]


class ICTTradingEnv(Env):
    """A lightweight trading environment suitable for RL training."""

    def __init__(
        self,
        observations: List[List[float]] | None,
        prices: List[Dict[str, Any]],
        config: Dict[str, float] | None = None,
        trade_log: List[Dict[str, float]] | None = None,
    ):
        self.prices = prices
        self.config = config or {}
        self.observations = observations or [[float(p.get("close", 0.0))] for p in prices]
        self.trade_log = trade_log or []
        self._index = 0
        self._done = False
        self._position = 0
        self._entry_price = 0.0
        self._equity = 0.0
        self._max_equity = 0.0
        self._last_trade_step = -9999
        obs_shape = (len(self.observations[0]),)
        self.observation_space = spaces.Box(
            low=-np.inf, high=np.inf, shape=obs_shape, dtype=np.float32
        )
        self.action_space = spaces.Discrete(len(Action))

    def reset(self, *, seed: int | None = None, options: Dict[str, Any] | None = None):
        super().reset(seed=seed)
        self._index = 0
        self._done = False
        self._position = 0
        self._entry_price = 0.0
        self._equity = 0.0
        self._max_equity = 0.0
        self._last_trade_step = -9999
        return np.array(self.observations[self._index], dtype=np.float32), {}

    def step(self, action: Action | int) -> Tuple[np.ndarray, float, bool, bool, Dict[str, float]]:
        if self._done:
            return (
                np.array(self.observations[self._index], dtype=np.float32),
                0.0,
                True,
                False,
                {"info": 0.0},
            )

        if isinstance(action, int):
            action = Action(action)

        price = float(self.prices[self._index].get("close", 0.0))
        risk_per_trade = float(self.config.get("risk_per_trade", 1.0))
        overtrade_window = int(self.config.get("overtrade_window", 3))
        drawdown_weight = float(self.config.get("drawdown_penalty_weight", 0.0))
        holding_penalty_value = float(self.config.get("holding_penalty", 0.0))

        trade_result = {"r_multiple": 0.0, "overtrade_penalty": 0.0}
        realized_pnl = 0.0

        if action == Action.BUY:
            if self._position <= 0:
                if self._position < 0:
                    realized_pnl = (self._entry_price - price)
                self._position = 1
                self._entry_price = price
                self._last_trade_step = self._index
        elif action == Action.SELL:
            if self._position >= 0:
                if self._position > 0:
                    realized_pnl = (price - self._entry_price)
                self._position = -1
                self._entry_price = price
                self._last_trade_step = self._index
        elif action == Action.CLOSE:
            if self._position != 0:
                realized_pnl = (price - self._entry_price) * self._position
                self._position = 0
                self._entry_price = 0.0
                self._last_trade_step = self._index

        if realized_pnl != 0.0:
            r_multiple = realized_pnl / risk_per_trade if risk_per_trade else 0.0
            trade_result["r_multiple"] = r_multiple
            self._equity += realized_pnl
            self._max_equity = max(self._max_equity, self._equity)
            self.trade_log.append({"r_multiple": r_multiple, "pnl": realized_pnl})

        if self._index - self._last_trade_step <= overtrade_window and realized_pnl != 0.0:
            trade_result["overtrade_penalty"] = float(self.config.get("overtrade_penalty", 0.0))

        drawdown = max(0.0, self._max_equity - self._equity)
        trade_result["drawdown_penalty"] = drawdown * drawdown_weight
        if self._position != 0:
            trade_result["holding_penalty"] = holding_penalty_value

        reward = calculate_reward(trade_result)

        self._index = min(self._index + 1, len(self.observations) - 1)
        if self._index >= len(self.observations) - 1:
            self._done = True

        info = {
            "r_multiple": trade_result["r_multiple"],
            "equity": self._equity,
            "position": float(self._position),
        }
        observation = np.array(self.observations[self._index], dtype=np.float32)
        return observation, reward, self._done, False, info
