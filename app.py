import streamlit as st
from data import get_data, compute_signal, compute_strategy_returns, calculate_metrics
import plotly.express as px
import pandas as pd

st.title("Moving Average Crossover Backtest")
st.subheader('Data from 01-01-2021 - 07-10-2026')

tickers = ["AAPL", "MSFT", "SPY", "META", "AMZN", "GOOGL", "NFLX", "TSLA", "WMT" ]
start_date = "2021-01-01"
end_date = "2026-07-10"

if tickers:
    close = get_data(tickers, str(start_date), str(end_date))
    position = compute_signal(close)
    strategy_returns, simple_returns = compute_strategy_returns(close, position)
    sharpe_ratio, max_drawdown = calculate_metrics(strategy_returns)

    st.write("Sharpe Ratio:")
    st.write("Sharpe ratio is measure of risk-adjusted return or how much return did we get for each unit " \
    "of risk we took on? Risk is calculated as the standard deviation of returns." \
    "A high Sharpe ratio means you're being efficiently compensated for the risk you're exposed to." \
    "A low Sharpe ratio means you're taking on risk without getting adequately paid for it. ")
    st.write("Sharpe Formula:")
    st.latex(r"\text{Sharpe Ratio} = \frac{R_x - R_f}{\text{StdDev } R_x}")
    st.caption("Rx represents the expected portfolio return, Rf represents the risk free rate of return, StdDev Rx = Standard deviation" \
    "of portfolio return/volatility")
    st.write(sharpe_ratio)
    plot_data = pd.DataFrame({"Ticker": sharpe_ratio.index, "Sharpe Ratio": sharpe_ratio.values})
    fig = px.scatter(plot_data, x="Ticker", y="Sharpe Ratio", color = "Ticker",  title="Sharpe Ratio by Ticker")
    fig.update_layout(font=dict(size=20))
    fig.update_traces(marker_size = 30)
    st.plotly_chart(fig)
    
    st.write("Max Drawdown:")
    st.write("How far below your peak are you right now. Largest percent drop from peak to trough")
    st.write(max_drawdown)
    plot_data = pd.DataFrame({"Ticker": max_drawdown.index, "Sharpe Ratio": max_drawdown.values})
    fig = px.scatter(plot_data, x="Ticker", y="Max Drawdown", color = "Ticker",  title="Max Drawdown")
    fig.update_layout(font=dict(size=20))
    fig.update_traces(marker_size = 30)
    st.plotly_chart(fig)
  