import plotly.express as px

def crash_probability_chart(df):
    return px.bar(
        df,
        x="Firm",
        y="Crash_Probability",
        title="Firm-Level Crash Vulnerability"
    )

def backtest_performance(df):
    return px.scatter(
        df,
        x="Predicted_Prob",
        y="Return",
        title="Backtest: Predicted Crash Risk vs Actual Returns"
    )


