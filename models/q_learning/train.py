"""Train a lightweight Q-learning agent on synthetic ICT-like price data."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import List

import numpy as np

from environment.action_space import Action
from environment.ict_env import ICTTradingEnv


def build_observations(length: int = 800, seed: int = 42) -> List[List[float]]:
    """Create synthetic close-price observations for quick local training."""
    rng = np.random.default_rng(seed)
    drift = 0.02
    noise = rng.normal(0.0, 0.5, size=length)
    prices = 100.0 + np.cumsum(drift + noise)
    return [[float(p)] for p in prices]


def state_from_observation(obs: List[float]) -> int:
    """Map continuous close values to a coarse discrete state for tabular Q-learning."""
    close = obs[0]
    bucket = int(close // 2)  # coarse bucketing keeps table small and stable
    return max(0, min(199, bucket))


def train_q_learning(episodes: int, alpha: float, gamma: float, epsilon: float, seed: int) -> dict:
    observations = build_observations(seed=seed)
    n_states = 200
    n_actions = len(Action)
    q_table = np.zeros((n_states, n_actions), dtype=np.float64)

    rng = np.random.default_rng(seed)
    episode_rewards: list[float] = []

    for _ in range(episodes):
        env = ICTTradingEnv(observations=observations)
        state = state_from_observation(env.reset())
        done = False
        total_reward = 0.0

        while not done:
            if rng.uniform() < epsilon:
                action_idx = int(rng.integers(0, n_actions))
            else:
                action_idx = int(np.argmax(q_table[state]))

            action = Action(action_idx)
            next_obs, reward, done, _ = env.step(action)
            next_state = state_from_observation(next_obs)

            best_next = float(np.max(q_table[next_state]))
            q_old = q_table[state, action_idx]
            q_table[state, action_idx] = q_old + alpha * (reward + gamma * best_next - q_old)

            state = next_state
            total_reward += reward

        episode_rewards.append(total_reward)

    greedy_policy = {str(s): int(np.argmax(q_table[s])) for s in range(n_states)}
    return {
        "episodes": episodes,
        "alpha": alpha,
        "gamma": gamma,
        "epsilon": epsilon,
        "avg_reward_last_50": float(np.mean(episode_rewards[-50:])),
        "avg_reward_all": float(np.mean(episode_rewards)),
        "q_table": q_table.tolist(),
        "greedy_policy": greedy_policy,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Train a tabular Q-learning policy for the ICT env.")
    parser.add_argument("--episodes", type=int, default=300)
    parser.add_argument("--alpha", type=float, default=0.1)
    parser.add_argument("--gamma", type=float, default=0.95)
    parser.add_argument("--epsilon", type=float, default=0.1)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--output", type=Path, default=Path("artifacts/q_learning_model.json"))
    args = parser.parse_args()

    result = train_q_learning(args.episodes, args.alpha, args.gamma, args.epsilon, args.seed)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2), encoding="utf-8")

    print(f"Training completed. Model saved to: {args.output}")
    print(f"Average reward (all episodes): {result['avg_reward_all']:.4f}")
    print(f"Average reward (last 50): {result['avg_reward_last_50']:.4f}")


if __name__ == "__main__":
    main()
