import plotly.express as px

def crash_probability_chart(df):
    return px.bar(
        df,
        x="Firm",
        y="Crash_Probability",
        title="Firm-Level Crash Vulnerability"
    )

import plotly.express as px

def backtest_performance(df):
    # SAFETY CHECKS (THIS FIXES YOUR ERROR)
    required_cols = {"Predicted_Prob", "Return"}

    if df is None or df.empty:
        return None

    if not required_cols.issubset(df.columns):
        return None

    return px.scatter(
        df,
        x="Predicted_Prob",
        y="Return",
        title="Backtest: Predicted Crash Risk vs Actual Returns",
        labels={
            "Predicted_Prob": "Predicted Crash Probability",
            "Return": "Actual Return"
        }
    )



