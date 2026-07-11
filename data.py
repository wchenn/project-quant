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
print(short_ma.head(5), long_ma.head(100))
'''is recent avg change (last 20 days) greater than long-term avg change? (last 100 days). 
this is a boolean, T means on this date, 20 day avg is higher than 100 day, false 20 day avg is lower
or equal to 100 day avg'''
signal = short_ma > long_ma
print('SIGNAL HERE')
print(signal.head(105))
position = signal.shift(1)
strategy_returns = position * simple_returns
# print(strategy_returns.head(10))
print(strategy_returns.iloc[100:115])

cumulative_returns = (1 + strategy_returns).cumprod()
buyhold_cumulative = (1 + simple_returns).cumprod()
'''active trading rule vs. passive holding '''
print(cumulative_returns.tail())
print(buyhold_cumulative.tail())

'''sharpe ratio -measure of risk-adjusted return, how much return did we 
get for each unit of risk we took on? Risk is calculated as the standard deviation of returns.
or how much return are you getting relative to risk'''

mean_daily_return = strategy_returns.mean()
std_daily_return = strategy_returns.std()
sharpe_ratio = (mean_daily_return / std_daily_return) * (252 ** 0.5)
print("Strategy Sharpe:")
print(sharpe_ratio)

buyhold_mean = simple_returns.mean()
buyhold_std = simple_returns.std()
buyhold_sharpe = (buyhold_mean / buyhold_std) * (252 ** 0.5)
print("Buy-and-hold Sharpe:")
print(buyhold_sharpe)