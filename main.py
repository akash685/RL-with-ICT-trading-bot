"""Entry point for running the ICT trading system pipeline."""
from __future__ import annotations

from features import (
    compute_fair_value_gaps,
    compute_indicators,
    compute_liquidity,
    compute_market_structure,
    compute_order_blocks,
    compute_premium_discount,
    compute_smt_divergence,
    encode_sessions,
)
from strategies import generate_sweep_mss_ob_signals


def run_pipeline(data, config):
    """Run a minimal feature + strategy pipeline on input data."""
    features = compute_market_structure(data, config)
    features = compute_liquidity(features, config)
    features = compute_order_blocks(features, config)
    features = compute_fair_value_gaps(features, config)
    features = compute_premium_discount(features, config)
    features = encode_sessions(features, config)
    features = compute_smt_divergence(features, config)
    features = compute_indicators(features, config)
    signals = generate_sweep_mss_ob_signals(features, config)
    return signals


if __name__ == "__main__":
    print("ICT trading system scaffold is ready. Integrate data loaders to run.")
