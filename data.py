import yfinance as yf
import numpy as np


def get_data(tickers, start_date, end_date):
    data = yf.download(tickers, start=start_date, end=end_date)
    return data['Close']

def compute_signal(close, short_window=20, long_window=100):
    shortma = close.rolling(short_window).mean()
    longma = close.rolling(long_window).mean()
    signal = shortma > longma
    position = signal.shift(1)
    return position

def compute_strategy_returns(close, position):
    simple_returns = close.pct_change()
    strategy_returns = position * simple_returns
    return strategy_returns, simple_returns


def calculate_metrics(strategy_returns): #returning Sharpe ratio and max drawdown
    mean_daily_return = strategy_returns.mean()
    std_daily_return = strategy_returns.std()
    sharpe_ratio = (mean_daily_return / std_daily_return) * (252 **.5)
    cumulative_returns = (1 + strategy_returns).cumprod()
    running_max = cumulative_returns.cummax()
    drawdown = (cumulative_returns - running_max) /running_max
    max_drawdown = drawdown.min() #biggest loss 
    return sharpe_ratio, max_drawdown

def apply_transaction_costs(position, strategy_returns, cost_pct=0.001):


close = get_data(["AAPL", "MSFT", "SPY"], "2021-01-01", "2026-07-10")
position = compute_signal(close)
strategy_returns, simple_returns = compute_strategy_returns(close, position)
sharpe_ratio, max_drawdown = calculate_metrics(strategy_returns)




print("Sharpe:", sharpe_ratio)
print("Max Drawdown:", max_drawdown)
buyhold_sharpe, buyhold_drawdown = calculate_metrics(simple_returns)

print("Buy-Hold Sharpe:", buyhold_sharpe)
print("Buy-Hold Max Drawdown:", buyhold_drawdown)






























# data = yf.download(["SPY", "AAPL", "MSFT"], start="2021-01-01", end="2026-07-10")
# close = data['Close']
# # print(close.index.is_monotonic_increasing) True
# # print(close.isna().sum()) No NA values
# '''simple returns: what percentage did the price change relative to yesterday's price?'''
# simple_returns = close.pct_change() 
# print(simple_returns.head())
# '''log returns: if this were growing continuously 
# (like continuously-compounding interest) rather than in
#  one discrete daily jump, what constant rate would produc
#  e this same price change?
#  -additive across time'''
# log_returns = np.log(close / close.shift(1))
# print(log_returns.head())
# total_log_return = log_returns['SPY'].sum()
# implied_log_return = np.log(close['SPY'].iloc[-1] / close['SPY'].iloc[0])
# print(total_log_return, implied_log_return)
# short_ma = close.rolling(window=20).mean()
# long_ma = close.rolling(window=100).mean()
# print(short_ma.head(5), long_ma.head(100))
# '''is recent avg change (last 20 days) greater than long-term avg change? (last 100 days). 
# this is a boolean, T means on this date, 20 day avg is higher than 100 day, false 20 day avg is lower
# or equal to 100 day avg'''
# signal = short_ma > long_ma
# print('SIGNAL HERE')
# print(signal.head(105))
# position = signal.shift(1)
# strategy_returns = position * simple_returns
# # print(strategy_returns.head(10))
# print(strategy_returns.iloc[100:115])

# cumulative_returns = (1 + strategy_returns).cumprod()
# buyhold_cumulative = (1 + simple_returns).cumprod()
# '''active trading rule vs. passive holding '''
# print(cumulative_returns.tail())
# print(buyhold_cumulative.tail())

# '''sharpe ratio -measure of risk-adjusted return, how much return did we 
# get for each unit of risk we took on? Risk is calculated as the standard deviation of returns.
# or how much return are you getting relative to risk higher Sharpe ratio means an investment 
# is generating greater returns for each unit of risk it takes on.
#  A high Sharpe ratio means you're being efficiently compensated for the risk you're exposed to. 
#  A low Sharpe ratio means you're taking on risk without getting adequately paid for it. 
#  stability is just std'''

# mean_daily_return = strategy_returns.mean()
# std_daily_return = strategy_returns.std()
# sharpe_ratio = (mean_daily_return / std_daily_return) * (252 ** 0.5)
# print("Strategy Sharpe:")
# print(sharpe_ratio)

# buyhold_mean = simple_returns.mean()
# buyhold_std = simple_returns.std()
# buyhold_sharpe = (buyhold_mean / buyhold_std) * (252 ** 0.5)
# print("Buy-and-hold Sharpe:")
# print(buyhold_sharpe)
# '''If today IS the peak (today's value equals the running max) → today's value - today's value = 0
# If today is BELOW the peak (running max was set on some earlier day) → smaller number - bigger number 
# = negative
# these numbers will be negative because we are comparing any valuable against their running maximum
# Drawdown is 0 at the moment you're sitting at a new peak, only negative or zero'''
# running_max = cumulative_returns.cummax()
# drawdown = (cumulative_returns - running_max) / running_max
# max_drawdown = drawdown.min()
# print("Strategy max drawdown:")
# print(max_drawdown)

# buyhold_running_max = buyhold_cumulative.cummax()
# buyhold_drawdown = (buyhold_cumulative - buyhold_running_max) / buyhold_running_max
# buyhold_max_drawdown = buyhold_drawdown.min()
# print("Buy-and-hold max drawdown:")
# print(buyhold_max_drawdown)

# worst_day = drawdown['AAPL'].idxmin()
# print(worst_day)
# print(drawdown['AAPL'].loc[worst_day])
# print(drawdown['MSFT'].loc[worst_day])
# print(drawdown['SPY'].loc[worst_day])

# trades = position.diff()
# print(trades.head(110))

# transaction_cost_pct = 0.001  # 0.1% (10 bps) per trade, a reasonable assumption (fees)
# cost = trades.abs() * transaction_cost_pct
# strategy_returns_after_costs = strategy_returns - cost
# print("Strategy returns after costs:")
# print(cost.head(110))
# print(strategy_returns_after_costs.head(110))
# print(trades.iloc[100:130])

# cumulative_after_costs = (1 + strategy_returns_after_costs).cumprod()
# print(cumulative_after_costs.tail())

# mean_after_costs = strategy_returns_after_costs.mean()
# std_after_costs = strategy_returns_after_costs.std()
# sharpe_after_costs = (mean_after_costs / std_after_costs) * (252 ** 0.5)
# print("Strategy Sharpe after costs:")
# print(sharpe_after_costs)

# '''back test here'''
# train_close = close.loc[:"2023-12-31"]
# test_close = close.loc["2024-01-01":]

# print(train_close.index.min(), train_close.index.max())
# print(test_close.index.min(), test_close.index.max())


# # Compute on the FULL dataset first, so rolling windows have complete history
# full_short_ma = close.rolling(window=20).mean()
# full_long_ma = close.rolling(window=100).mean()
# full_signal = full_short_ma > full_long_ma
# full_position = full_signal.shift(1)
# full_strategy_returns = full_position * simple_returns

# # THEN slice the already-computed results into train/test
# train_strategy_returns = full_strategy_returns.loc[:"2023-12-31"]
# test_strategy_returns = full_strategy_returns.loc["2024-01-01":]

# train_mean = train_strategy_returns.mean()
# train_std = train_strategy_returns.std()
# train_sharpe = (train_mean / train_std) * (252 ** 0.5)
# print("Train Sharpe (2021-2023):")
# print(train_sharpe)

# test_mean = test_strategy_returns.mean()
# test_std = test_strategy_returns.std()
# test_sharpe = (test_mean / test_std) * (252 ** 0.5)
# print("Test Sharpe (2024-2026):")
# print(test_sharpe)

