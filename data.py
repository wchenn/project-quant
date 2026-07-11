import yfinance as yf
import numpy as np


data = yf.download(["SPY", "AAPL", "MSFT"], start="2021-01-01", end="2026-07-10")
close = data['Close']
# print(close.index.is_monotonic_increasing) True
# print(close.isna().sum()) No NA values
'''simple returns: what percentage did the price change relative to yesterday's price?'''
simple_returns = close.pct_change() 
print(simple_returns.head())
'''log returns: if this were growing continuously 
(like continuously-compounding interest) rather than in
 one discrete daily jump, what constant rate would produc
 e this same price change?
 -additive across time'''
log_returns = np.log(close / close.shift(1))
print(log_returns.head())
total_log_return = log_returns['SPY'].sum()
implied_log_return = np.log(close['SPY'].iloc[-1] / close['SPY'].iloc[0])
print(total_log_return, implied_log_return)
short_ma = close.rolling(window=20).mean()
long_ma = close.rolling(window=100).mean()
print(short_ma.head(5), long_ma.head(1005))
signal = short_ma > long_ma
print(signal.head(105))
position = signal.shift(1)
strategy_returns = position * simple_returns
# print(strategy_returns.head(10))
print(strategy_returns.iloc[100:115])

