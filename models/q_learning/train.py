"""Train a lightweight Q-learning agent on real market data."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import List
from urllib.error import URLError

import numpy as np
import pandas as pd

from environment.action_space import Action
from environment.ict_env import ICTTradingEnv

DEFAULT_STOOQ_URL = "https://stooq.com/q/d/l/?s={symbol}&i=d"


def load_real_close_prices(symbol: str, source_csv: str | None = None, limit: int = 1500) -> pd.DataFrame:
    """Load daily OHLC data from CSV path/URL and return ascending dataframe."""
    fallback_csv = Path("data/spy_sample_daily.csv")

    if source_csv:
        df = pd.read_csv(source_csv)
        source = source_csv
    else:
        source = DEFAULT_STOOQ_URL.format(symbol=symbol)
        try:
            df = pd.read_csv(source)
        except (URLError, OSError):
            if not fallback_csv.exists():
                raise
            df = pd.read_csv(fallback_csv)
            source = str(fallback_csv)

    required = {"Date", "Open", "High", "Low", "Close"}
    missing = required.difference(df.columns)
    if missing:
        raise ValueError(f"Missing required columns from data source: {sorted(missing)}")

    cleaned = (
        df.dropna(subset=["Date", "Close"])
        .assign(Date=lambda x: pd.to_datetime(x["Date"], errors="coerce"))
        .dropna(subset=["Date"])
        .sort_values("Date")
        .tail(limit)
        .reset_index(drop=True)
    )
    if len(cleaned) < 2:
        raise ValueError("Need at least two bars of real data for training.")

    cleaned.attrs["source"] = source
    return cleaned


def build_observations_from_prices(price_df: pd.DataFrame) -> List[List[float]]:
    """Build environment observations from close prices."""
    return [[float(close)] for close in price_df["Close"].tolist()]


def state_from_observation(obs: List[float]) -> int:
    """Map continuous close values to a coarse discrete state for tabular Q-learning."""
    close = obs[0]
    bucket = int(close // 2)
    return max(0, min(199, bucket))


def train_q_learning(
    episodes: int,
    alpha: float,
    gamma: float,
    epsilon: float,
    seed: int,
    observations: List[List[float]],
) -> dict:
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
    parser.add_argument("--symbol", type=str, default="spy.us", help="Stooq symbol (default: spy.us)")
    parser.add_argument("--source-csv", type=str, default=None, help="Optional local CSV or URL with OHLC columns")
    parser.add_argument("--max-bars", type=int, default=1500)
    parser.add_argument("--output", type=Path, default=Path("artifacts/q_learning_model.json"))
    args = parser.parse_args()

    price_df = load_real_close_prices(symbol=args.symbol, source_csv=args.source_csv, limit=args.max_bars)
    observations = build_observations_from_prices(price_df)
    result = train_q_learning(args.episodes, args.alpha, args.gamma, args.epsilon, args.seed, observations)

    result["data"] = {
        "symbol": args.symbol,
        "source": price_df.attrs.get("source", "unknown"),
        "bars": int(len(price_df)),
        "start": str(price_df["Date"].iloc[0].date()),
        "end": str(price_df["Date"].iloc[-1].date()),
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2), encoding="utf-8")

    print(f"Training completed. Model saved to: {args.output}")
    print(f"Data source: {result['data']['source']}")
    print(f"Bars: {result['data']['bars']} ({result['data']['start']} -> {result['data']['end']})")
    print(f"Average reward (all episodes): {result['avg_reward_all']:.4f}")
    print(f"Average reward (last 50): {result['avg_reward_last_50']:.4f}")


if __name__ == "__main__":
    main()
