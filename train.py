"""Train an RL agent on ICT features."""
from __future__ import annotations

import argparse
from typing import Any, Dict

import pandas as pd

from data.loader import build_observations, compute_feature_frame, load_ohlcv_csv
from environment.ict_env import ICTTradingEnv


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train an RL agent on ICT features.")
    parser.add_argument("--data", required=True, help="Path to OHLCV CSV file.")
    parser.add_argument("--timesteps", type=int, default=10_000, help="Training timesteps.")
    parser.add_argument("--model", default="ppo", choices=["ppo"], help="RL algorithm.")
    parser.add_argument("--save-path", default="models/trained_agent.zip", help="Output path.")
    parser.add_argument("--timezone", default="UTC", help="Timezone for timestamps.")
    return parser.parse_args()


def build_env(data: pd.DataFrame, config: Dict[str, Any]) -> ICTTradingEnv:
    features = compute_feature_frame(data, config)
    feature_columns = config.get("feature_columns")
    observations = build_observations(features, feature_columns)
    prices = data[["close"]].to_dict(orient="records")
    return ICTTradingEnv(observations=observations, prices=prices, config=config)


def train_agent(args: argparse.Namespace) -> None:
    config: Dict[str, Any] = {
        "risk_per_trade": 1.0,
        "overtrade_window": 3,
        "overtrade_penalty": 0.0,
        "drawdown_penalty_weight": 0.0,
        "holding_penalty": 0.0,
    }
    data = load_ohlcv_csv(args.data, timezone=args.timezone)
    env = build_env(data, config)

    if args.model == "ppo":
        from stable_baselines3 import PPO

        model = PPO("MlpPolicy", env, verbose=1)
    else:
        raise ValueError(f"Unsupported model: {args.model}")

    model.learn(total_timesteps=args.timesteps)
    model.save(args.save_path)


if __name__ == "__main__":
    train_agent(parse_args())
