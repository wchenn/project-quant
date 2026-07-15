import streamlit as st
from data import get_data, compute_signal, compute_strategy_returns, calculate_metrics, apply_transaction_costs
import plotly.express as px
import pandas as pd



st.set_page_config(
    page_title="Moving Average Crossover Backtest",
    page_icon="📈",
    layout="wide"
)
st.title("Moving Average Crossover Backtest")
st.subheader('Intro')
st.write("""Hello, I'm Will. This project is a backtesting engine that tests a simple moving-average crossover trading strategy (20/100 MA) against several stocks (AAPL, MSFT, AMZN, and others) from 2021–2026, comparing it to a simple buy-and-hold approach. I built this to deepen my understanding of quantitative finance and Python, evaluating the strategy using risk-adjusted metrics like Sharpe ratio and maximum drawdown, and testing whether results held up across different time periods.
Key finding: the moving-average strategy generally underperformed simple buy-and-hold on both raw return and risk-adjusted return (Sharpe ratio) across most tickers tested. Its apparent edge was also unstable across different time periods — for example, one ticker's Sharpe ratio dropped from 0.59 in 2021–2023 to just 0.02 in 2024–2026 — suggesting the strategy's performance is highly sensitive to market conditions rather than reflecting a durable, repeatable pattern.
Note: this analysis uses a fixed dataset (Jan 2021 to July 2026) rather than live-updating dates, so results are reproducible and won't drift over time.  The stack used for this project included: Python, Pandas, Numpy, Yahoo Finance API, Plotly and Streamlit""")

st.info("""
Ultimately - Across 6 tickers tested (01/01/2021 to 07/10/2026), a 20/100 moving-average crossover strategy (purchase when the shorter term mass average is > the long term mass average and sell/exit when the inverse is true)
underperformed simple buy-and-hold on both raw return and Sharpe ratio for most stocks. Performance was also unstable across different time periods, suggesting the strategy lacks a durable edge.
""")


tickers = ["AAPL", "MSFT", "META", "AMZN", "GOOGL", "NFLX"]
start_date = "2021-01-01"
end_date = "2026-07-10"

if tickers:
    close = get_data(tickers, str(start_date), str(end_date))
    position = compute_signal(close)
    strategy_returns, simple_returns = compute_strategy_returns(close, position)
    strategy_returns_after_cost = apply_transaction_costs(position, strategy_returns)

    sharpe_after_costs, drawdown_after_costs = calculate_metrics(strategy_returns_after_cost)
    sharpe_ratio, max_drawdown = calculate_metrics(strategy_returns)

    buyhold_sharpe, buyhold_drawdown = calculate_metrics(simple_returns)

    st.subheader("Sharpe Ratio")
    st.write("Sharpe ratio is measure of risk-adjusted return or how much return did we get for each unit " \
    "of risk we took on? Risk is calculated as the standard deviation of returns." \
    "A high Sharpe ratio means you're being efficiently compensated for the risk you're exposed to." \
    "A low Sharpe ratio means you're taking on risk without getting adequately paid for it. ")
    st.write("Sharpe Formula:")
    st.latex(r"\text{Sharpe Ratio} = \frac{R_x - R_f}{\text{StdDev } R_x}")
    st.caption('<div style="text-align: center">Rx represents the expected portfolio return, Rf represents the risk free rate of return, StdDev Rx = Standard deviation \
     of portfolio return/volatility</div>', unsafe_allow_html=True)
    st.write(sharpe_ratio)
    st.write('''AMZN's negative Sharpe ratio means its strategy's average daily return was negative — it lost money on average, rather than underperforming a specific benchmark 
             rate. The opposite is true for META: its positive Sharpe ratio reflects a positive average daily return, and its comparatively high magnitude suggests that return was earned efficiently relative to the volatility involved.''')


    plot_data = pd.DataFrame({"Ticker": sharpe_ratio.index, "Sharpe Ratio": sharpe_ratio.values})
    fig = px.scatter(plot_data, x="Ticker", y="Sharpe Ratio", color = "Ticker",  title="Sharpe Ratio by Ticker")
    fig.update_layout(font=dict(size=20))
    fig.update_traces(marker_size = 30)
    st.plotly_chart(fig)
    
    st.subheader("Max Drawdown")
    # st.write("Max Drawdown:")
    st.write("""Maximum Drawdown (Max DD) is the single largest "peak-to-trough" drop in a trading strategy's value before a new high is reached. It represents the worst-case historical loss you would have experienced if you invested at the top and sold at the bottom of that decline.""")

    st.write("""Two strategies can earn similar returns while one experiences a much deeper decline along the way. Because of this, Max Drawdown can also be used to judge whether the profit earned was worth the historical stress required to achieve it — a concept closely related to the Calmar Ratio.""")


    df = pd.DataFrame ({'xdata' : [1, 2, 3, 4, 5, 6, 7], 'ydata' : [15,40, 89, 159, 23, -16, 20]})
    fig = px.line(df, x = 'xdata' , y = 'ydata', title ="Peak and Trough Example")
    fig.add_annotation(x = 4, y=159, text = "Peak")
    fig.add_annotation(x = 6, y=-16, text = "Trough")
    st.plotly_chart(fig)


    st.latex(r"\text{Drawdown} = \frac{\text{Peak Value} - \text{Trough Value}}{\text{Peak Value}}")

    st.write(max_drawdown)
    plot_data = pd.DataFrame({"Ticker": max_drawdown.index, "Max Drawdown": max_drawdown.values})
    fig = px.scatter(plot_data, x="Ticker", y="Max Drawdown", color = "Ticker",  title="Max Drawdown")
    fig.update_layout(font=dict(size=20))
    fig.update_traces(marker_size = 30)
    st.plotly_chart(fig)
  
    cumulative_returns = (1 + strategy_returns).cumprod()
    buyhold_cumulative = (1 + simple_returns).cumprod()
    cumulative_returns_pct = (cumulative_returns - 1) * 100
    buyhold_cumulative_pct = (buyhold_cumulative - 1) * 100
    st.write('Cumulative Returns - only buying when short ma > long ma')
    st.line_chart(cumulative_returns_pct, y_label= '%')
    st.write('Buy Hold Cumulative')
    st.line_chart(buyhold_cumulative_pct, y_label= '%')
    st.subheader("Summary")

    table_data = pd.DataFrame({
        "Strategy Sharpe": sharpe_ratio,
        "Sharpe with Transaction Cost": sharpe_after_costs,
        "Buy-Hold Sharpe": buyhold_sharpe,
        "Strategy Return %": cumulative_returns_pct.iloc[-1],
        "Buy-Hold Return %": buyhold_cumulative_pct.iloc[-1],
        "Strategy Drawdown": max_drawdown,
        "Buy-Hold Drawdown": buyhold_drawdown
})
    st.caption('Transaction Costs of 10 bps (.001) to simulate transaction fees since we are selling when long MA>short MA in the strategy')
    st.write(table_data)


