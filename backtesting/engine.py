"""Backtest engine skeleton."""
from __future__ import annotations

from typing import Any, Dict, List

from .metrics import compute_metrics


def run_backtest(
    signals: List[Dict[str, Any]], prices: List[Dict[str, Any]], config: Dict[str, Any]
) -> Dict[str, float]:
    """Run a simple backtest loop.

    Args:
        signals: List of signal dicts.
        prices: List of price dicts.
        config: Backtest configuration.

    Returns:
        Summary metrics.
    """
    risk_per_trade = float(config.get("risk_per_trade", 1.0))
    close_on_flat = bool(config.get("close_on_flat", False))

    position = 0
    entry_price = 0.0
    trades: List[Dict[str, float]] = []

    for signal, price in zip(signals, prices):
        close_price = float(price.get("close", 0.0))
        signal_value = int(signal.get("signal", 0))

        if signal_value == 1 and position <= 0:
            if position < 0:
                pnl = entry_price - close_price
                trades.append(
                    {"pnl": pnl, "r_multiple": pnl / risk_per_trade if risk_per_trade else 0.0}
                )
            position = 1
            entry_price = close_price
        elif signal_value == -1 and position >= 0:
            if position > 0:
                pnl = close_price - entry_price
                trades.append(
                    {"pnl": pnl, "r_multiple": pnl / risk_per_trade if risk_per_trade else 0.0}
                )
            position = -1
            entry_price = close_price
        elif signal_value == 0 and close_on_flat and position != 0:
            pnl = (close_price - entry_price) * position
            trades.append(
                {"pnl": pnl, "r_multiple": pnl / risk_per_trade if risk_per_trade else 0.0}
            )
            position = 0
            entry_price = 0.0

    if position != 0:
        final_price = float(prices[-1].get("close", 0.0))
        pnl = (final_price - entry_price) * position
        trades.append({"pnl": pnl, "r_multiple": pnl / risk_per_trade if risk_per_trade else 0.0})

    return compute_metrics(trades)
