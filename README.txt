# Moving Average Crossover Backtest

Will Chen | https://www.linkedin.com/in/william-chen-5456261a9/ | https://wchenbacktesting.streamlit.app/

## Overview
This project is a backtesting engine that tests a simple moving-average crossover trading strategy (20/100 MA) against several stocks (AAPL, MSFT, SPY, and others) from 2021–2026, comparing it to a simple buy-and-hold approach. 


## Key Finding
Across 6 tickers tested (01/01/2021 to 07/10/2026), a 20/100 moving-average crossover strategy (purchase when the shorter term mass average is > the long term mass average and sell/exit when the inverse is true) underperformed simple buy-and-hold on both raw return and Sharpe ratio for most stocks. Performance was also unstable across different time periods, suggesting the strategy lacks a durable edge.


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
