# Moving Average Crossover Backtest

Will Chen | https://www.linkedin.com/in/william-chen-5456261a9/ | asdooasnf.com/asdf2

## Overview
[Your existing intro paragraph — keep as-is, it's good]

## Key Finding
[Your existing key finding paragraph — keep as-is]

## Methodology
- Data: daily closing prices for AAPL, MSFT, SPY, META, AMZN, GOOGL, NFLX, TSLA, WMT, JPM (Jan 2021–July 2026), pulled via yfinance
- Strategy: 20-day / 100-day moving average crossover — long when short MA > long MA, flat otherwise
- Signal is shifted forward one day before trading to avoid look-ahead bias
- Benchmarked against simple buy-and-hold on the same tickers/period
- Metrics: Sharpe ratio (annualized), maximum drawdown
- Transaction costs: 10 bps per trade applied to test realistic trading friction
- Robustness check: split the data into train (2021–2023) and test (2024–2026) periods to check whether performance was stable across different market regimes

## Limitations
- Single-asset backtests, not a portfolio-level analysis
- Fixed 20/100 window — not tuned or optimized, chosen as a common convention
- Flat transaction cost assumption (10 bps), doesn't model slippage or bid-ask spread dynamically
- Fixed date range (not live-updating) — see note above

## How to Run
1. Clone this repo
2. `pip install -r requirements.txt`
3. `streamlit run app.py`

## Tech Stack
Python, pandas, numpy, yfinance, Streamlit, Plotly
