import streamlit as st
from data import get_data, compute_signal, compute_strategy_returns, calculate_metrics
import plotly.express as px
import pandas as pd



st.set_page_config(
    page_title="Moving Average Crossover Backtest",
    page_icon="📈",
    layout="wide"
)
st.title("Moving Average Crossover Backtest")
st.subheader('Intro')
st.write("""Hello, I'm Will. This project is a backtesting engine that tests a simple moving-average crossover trading strategy (20/100 MA) against several stocks (AAPL, MSFT, SPY, and others) from 2021–2026, comparing it to a simple buy-and-hold approach. I built this to deepen my understanding of quantitative finance and Python, evaluating the strategy using risk-adjusted metrics like Sharpe ratio and maximum drawdown, and testing whether results held up across different time periods.
Key finding: the moving-average strategy generally underperformed simple buy-and-hold on both raw return and risk-adjusted return (Sharpe ratio) across most tickers tested. Its apparent edge was also unstable across different time periods — for example, one ticker's Sharpe ratio dropped from 0.59 in 2021–2023 to just 0.02 in 2024–2026 — suggesting the strategy's performance is highly sensitive to market conditions rather than reflecting a durable, repeatable pattern.
Note: this analysis uses a fixed dataset (Jan 2021 to July 2026) rather than live-updating dates, so results are reproducible and won't drift over time.  The stack used for this project included: Python, Pandas, Numpy, Yahoo Finance API, Plotly and Streamlit""")

st.info("""
**TL;DR:** Across 10 tickers tested (01/01/2021 to 07/10/2026), a 20/100 moving-average crossover strategy (purchase when the shorter term mass average is > the long term mass average)
underperformed simple buy-and-hold on both raw return and Sharpe ratio for most stocks. Performance was also unstable across different time periods, suggesting the strategy lacks a durable edge.
""")


tickers = ["AAPL", "MSFT", "META", "AMZN", "GOOGL", "NFLX"]
start_date = "2021-01-01"
end_date = "2026-07-10"

if tickers:
    close = get_data(tickers, str(start_date), str(end_date))
    position = compute_signal(close)
    strategy_returns, simple_returns = compute_strategy_returns(close, position)
    sharpe_ratio, max_drawdown = calculate_metrics(strategy_returns)
    buyhold_sharpe, buyhold_drawdown = calculate_metrics(simple_returns)

    st.subheader("Sharpe Ratio")
    st.write("Sharpe ratio is measure of risk-adjusted return or how much return did we get for each unit " \
    "of risk we took on? Risk is calculated as the standard deviation of returns." \
    "A high Sharpe ratio means you're being efficiently compensated for the risk you're exposed to." \
    "A low Sharpe ratio means you're taking on risk without getting adequately paid for it. ")
    st.write("Sharpe Formula:")
    st.latex(r"\text{Sharpe Ratio} = \frac{R_x - R_f}{\text{StdDev } R_x}")
    st.caption('<div style="text-align: center">Rx represents the expected portfolio return, Rf represents the risk free rate of return, StdDev Rx = Standard deviation" \
    " of portfolio return/volatility</div>', unsafe_allow_html=True)
    st.write(sharpe_ratio)
    st.write('''We see above that META has the strongest Sharpe Ratio of the stocks selected. You would expect high rewards for every unit of volatility 
             calculated by the Sharpe Formula.  While the worse one here is AMZN.  AMZN's negative Sharpe ratio indicates that the return is lower than the risk free rate (the investment lost money)''')


    plot_data = pd.DataFrame({"Ticker": sharpe_ratio.index, "Sharpe Ratio": sharpe_ratio.values})
    fig = px.scatter(plot_data, x="Ticker", y="Sharpe Ratio", color = "Ticker",  title="Sharpe Ratio by Ticker")
    fig.update_layout(font=dict(size=20))
    fig.update_traces(marker_size = 30)
    st.plotly_chart(fig)
    
    st.subheader("Max Drawdown")
    # st.write("Max Drawdown:")
    st.write("Max Drawdown measures worst case hisorical loss.  This is typically used to evaluate an asset's downside risk and volatility. In other words how far below the peak are you right now. " \
    "Largest percent drop from peak to trough negative a percentage drop is, the larger and more severe the price decline" \
    )
    st.write("Example of a peak and a trough")
    df = pd.DataFrame ({'xdata' : [1, 2, 3, 4, 5, 6, 7], 'ydata' : [15,40, 89, 159, 23, -16, 20]})
    fig = px.line(df, x = 'xdata' , y = 'ydata', title ="Peak and Trough Example")
    fig.add_annotation(x = 4, y=159, text = "Peak")
    fig.add_annotation(x = 6, y=-16, text = "Trough")
    st.plotly_chart(fig)


    st.latex(r"\text{Drawdown} = \frac{\text{Peak Value} - \text{Trough Value}}{\text{Peak Value}}")
    st.caption('<div style="text-align: center">Max Drawdown</div>', unsafe_allow_html=True)

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
        "Buy-Hold Sharpe": buyhold_sharpe,
        "Strategy Return %": cumulative_returns_pct.iloc[-1],
        "Buy-Hold Return %": buyhold_cumulative_pct.iloc[-1],
        "Strategy Drawdown": max_drawdown,
        "Buy-Hold Drawdown": buyhold_drawdown
})
    st.write(table_data)


