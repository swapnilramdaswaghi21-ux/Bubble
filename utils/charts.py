import plotly.express as px

def crash_probability_chart(df):
    return px.bar(
        df,
        x="Firm",
        y="Crash_Probability",
        title="Firm-Level Crash Vulnerability"
    )

import plotly.express as px

import plotly.express as px

def backtest_performance(df):
    # REQUIRED COLUMNS
    required_cols = {"Predicted_Prob", "Return"}

    # SAFETY CHECKS
    if df is None or df.empty:
        return None

    if not required_cols.issubset(df.columns):
        return None

    # ENSURE NUMERIC
    df = df.copy()
    df["Predicted_Prob"] = df["Predicted_Prob"].astype(float)
    df["Return"] = df["Return"].astype(float)

    # REMOVE NaNs
    df = df.dropna(subset=["Predicted_Prob", "Return"])

    if df.empty:
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




