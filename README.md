# ICT + Reinforcement Learning Trading System Blueprint

This repository captures a full blueprint for combining **ICT (Inner Circle Trader) concepts** with **Reinforcement Learning (RL)** to build a professional trading system. It outlines the concepts to model, how to translate them into machine-learning features, RL environment design, a production-grade folder layout, and a step-by-step implementation roadmap.

## Part 1 — ICT Concepts to Model

### Market Structure

**Break of Structure (BOS)**
- Price breaks a previous high/low → continuation signal.

**Market Structure Shift (MSS)**
- Trend change signal.

**Suggested features**
- Swing high/low breaks
- Trend direction label
- Distance from last BOS

### Liquidity Concepts

**Buy-side Liquidity**
- Above equal highs.

**Sell-side Liquidity**
- Below equal lows.

**Liquidity Sweep / Stop Hunt**

**Suggested features**
- Equal high/low clusters
- Sweep candle size
- Reversal speed after sweep

### Order Flow

**Order Blocks (OB)**
- Last bullish/bearish candle before an impulse move.

Types
- Bullish OB
- Bearish OB

**Suggested features**
- OB high/low range
- Reaction strength
- Time since OB formed

**Fair Value Gap (FVG / Imbalance)**
- Price inefficiency zones.

Types
- Bullish FVG
- Bearish FVG

**Suggested features**
- Gap size
- Filled or unfilled
- Entry precision

### Premium & Discount Zones

- Use Fibonacci of the recent swing:
  - Discount zone (buy area)
  - Premium zone (sell area)
  - 50% equilibrium

**Suggested features**
- Distance from equilibrium (EQ)
- Zone classification

### Kill Zones (Time-based edge)

High probability times:
- London open
- NY open
- NY lunch reversal

**Suggested features**
- Session encoding
- Volatility spike flag

### SMT Divergence (Smart Money Technique)

Compare correlated markets, for example:
- EURUSD vs DXY
- NASDAQ vs S&P 500

**Suggested features**
- Divergence magnitude
- Confirmation score

## Part 2 — ICT Strategies to Automate

### Strategy 1 — Liquidity Sweep + MSS + OB Entry
1. Price sweeps liquidity.
2. MSS confirms reversal.
3. Enter on Order Block.

### Strategy 2 — FVG Continuation
1. Trend via BOS.
2. Pullback into FVG.
3. Continue trend trade.

### Strategy 3 — Premium/Discount Reversal
1. Liquidity sweep in premium/discount.
2. OB + MSS confirmation.

### Strategy 4 — Killzone Momentum
- High-volatility entries with structure + FVG.

## Part 3 — RL System Design

### Agent Inputs (State)
- Market structure
- Liquidity zones
- Order block distances
- FVG presence
- Session time
- Volatility
- Trend strength
- Premium/discount percentage

### Agent Actions
- 0 = Hold
- 1 = Buy
- 2 = Sell
- 3 = Close trade

### Reward Function (Profit-optimized)
Reward is based on:
- ✅ Risk:Reward achieved
- ✅ Drawdown control
- ✅ Win streak bonus
- ❌ Overtrading penalty
- ❌ Holding during chop

Example:
- `+2R profit = +2`
- `-1R loss = -1`
- `Early exit profit = +0.5`

## Part 4 — Professional Folder Structure

```
ict_trading_bot/
│
├── data/
│   ├── raw/
│   │   ├── forex/
│   │   ├── crypto/
│   │   └── indices/
│   │
│   ├── cleaned/
│   ├── resampled/
│   └── labeled/
│
├── features/
│   ├── market_structure.py
│   ├── liquidity.py
│   ├── order_blocks.py
│   ├── fvg.py
│   ├── premium_discount.py
│   ├── sessions.py
│   ├── smt_divergence.py
│   └── indicators.py
│
├── strategies/
│   ├── sweep_mss_ob.py
│   ├── fvg_continuation.py
│   ├── premium_reversal.py
│   └── killzone_breakout.py
│
├── environment/
│   ├── ict_env.py
│   ├── reward.py
│   └── action_space.py
│
├── models/
│   ├── dqn/
│   ├── ppo/
│   ├── a2c/
│   └── trained_agents/
│
├── backtesting/
│   ├── engine.py
│   ├── metrics.py
│   └── plots.py
│
├── risk_management/
│   ├── position_size.py
│   ├── stop_loss.py
│   └── max_drawdown.py
│
├── execution/
│   ├── broker_api.py
│   ├── live_trader.py
│   └── paper_trader.py
│
├── configs/
│   ├── symbols.yaml
│   ├── risk.yaml
│   └── model_params.yaml
│
├── notebooks/
│   └── research.ipynb
│
├── main.py
└── requirements.txt
```

## Part 5 — Step-by-Step Development Plan

### Phase 1 — Data
- Get OHLCV data.
- Multi-timeframe (1m, 5m, 15m, 1h, 4h).

### Phase 2 — Feature Engineering (Most Important)
Build:
- Structure detector
- Liquidity mapper
- OB & FVG scanners

### Phase 3 — Strategy Logic (Rule-based First)
Before RL:
- Hard-code ICT strategies
- Confirm profitability

### Phase 4 — RL Training
Train the agent to:
- Choose best entries
- Skip bad setups
- Optimize TP/SL

### Phase 5 — Risk + Execution
- Capital protection layer

## Recommended RL Algorithms for Trading

| Algorithm | Use |
| --- | --- |
| PPO | Best stability |
| DQN | Simple discrete actions |
| A2C | Fast learning |
| SAC | Advanced |

## Part 6 — MVP Implementation Checklist

Use this checklist to move from blueprint to code with clear milestones.

### Data + Validation
- [ ] Choose a primary market and timeframe (ex: EURUSD 5m).
- [ ] Define session windows (London/NY) and time zone conversions.
- [ ] Build a data validation script (missing candles, duplicates, bad timestamps).

### Feature Contracts (Minimal Definitions)
- [ ] **Structure**: swing high/low detection with lookback `n`.
- [ ] **BOS/MSS**: label breaks and shifts with timestamp and direction.
- [ ] **Liquidity**: equal highs/lows cluster within tolerance `ε`.
- [ ] **Order Blocks**: last opposite-color candle before impulse and its range.
- [ ] **FVG**: detect gaps between candle `i-1` and `i+1`.
- [ ] **Premium/Discount**: compute 0-50-100 zones from latest swing.
- [ ] **Session Encoding**: one-hot for kill zones.

### Strategy Baselines (Rule-based)
- [ ] Encode 1–2 strategies end-to-end with fixed risk rules.
- [ ] Add a backtest harness that outputs: win rate, expectancy, max DD.

### RL Environment Skeleton
- [ ] Define observation vector schema with fixed ordering.
- [ ] Add a simple reward function (R-multiples only).
- [ ] Implement action masking (no short if already long).
- [ ] Log trades to a structured ledger (CSV/Parquet).

### Training + Evaluation
- [ ] Start with a single algorithm (PPO recommended).
- [ ] Use walk-forward splits (train/validation/test).
- [ ] Track out-of-sample metrics + stability across regimes.

## Part 7 — Suggested Interfaces (Optional)

These lightweight interface contracts make modules composable:

```text
features/
  compute_features(df, config) -> pd.DataFrame
strategies/
  generate_signals(features_df, config) -> pd.DataFrame
environment/
  class ICTTradingEnv(gym.Env)
    reset() -> observation
    step(action) -> observation, reward, done, info
backtesting/
  run_backtest(signals_df, prices_df, config) -> metrics
```

If you want, the next step can be a concrete feature module (BOS/MSS/FVG) with unit tests and a small sample dataset.

## Quick Local Training (Q-learning baseline)

You can now run a lightweight local training loop without external RL libraries:

```bash
python -m models.q_learning.train --episodes 300 --output artifacts/q_learning_model.json
```

This generates a JSON artifact containing the learned Q-table, summary rewards, and a greedy policy mapping.
