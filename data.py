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
    trades = position.diff()
    cost = trades.abs() * cost_pct
    strategy_returns_after_cost =strategy_returns - cost
    return strategy_returns_after_cost



close = get_data(["AAPL", "MSFT", "SPY"], "2021-01-01", "2026-07-10")
position = compute_signal(close)
strategy_returns, simple_returns = compute_strategy_returns(close, position)
sharpe_ratio, max_drawdown = calculate_metrics(strategy_returns)
posttrans = apply_transaction_costs(position, strategy_returns, cost_pct=.001)
train_strategy_returns = strategy_returns.loc[:"2023-12-31"]
test_strategy_returns = strategy_returns.loc["2024-01-01":]

train_sharpe, train_drawdown = calculate_metrics(train_strategy_returns)
test_sharpe, test_drawdown = calculate_metrics(test_strategy_returns)

print("Train Sharpe:", train_sharpe)
print("Test Sharpe:", test_sharpe)
print("Train Max Drawdown:", train_drawdown)
print("Test Max Drawdown:", test_drawdown) #testing to see if a pattern is consistent


print("Strategy Returns after Cost", posttrans)

print("Sharpe:", sharpe_ratio)
print("Max Drawdown:", max_drawdown)
buyhold_sharpe, buyhold_drawdown = calculate_metrics(simple_returns)

print("Buy-Hold Sharpe:", buyhold_sharpe)
print("Buy-Hold Max Drawdown:", buyhold_drawdown)
print(strategy_returns.loc["2021-06-24"])
print(posttrans.loc["2021-06-24"])





