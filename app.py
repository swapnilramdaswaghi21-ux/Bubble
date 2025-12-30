import streamlit as st
import pandas as pd

from utils.feature_engineering import build_features
from utils.ml_model import train_crash_model
from utils.backtesting import backtest_crashes
from utils.portfolio_risk import portfolio_stress
from utils.charts import crash_probability_chart, backtest_performance

st.set_page_config(layout="wide")
st.title("📉 Bubble, Crash & Portfolio Stress Radar")

# ---------------- LOAD DATA ----------------
df = pd.read_csv("data/example_panel_with_prices.csv")

industry = st.selectbox("Select Industry", df["Industry"].unique())
df_i = df[df["Industry"] == industry]

# ---------------- TRAIN MODEL ----------------
features = build_features(df_i)
model = train_crash_model(df_i, features)

df_latest = df_i[df_i["Year"] == df_i["Year"].max()].copy()
df_latest["Crash_Probability"] = model.predict_proba(
    build_features(df_latest)
)[:,1]

df_latest = df_latest.sort_values("Crash_Probability", ascending=False)

# ---------------- DISPLAY RISK ----------------
st.subheader("🚨 Firms Most Likely to Crack First")
st.dataframe(
    df_latest[["Firm", "Crash_Probability"]],
    use_container_width=True
)

st.plotly_chart(crash_probability_chart(df_latest), use_container_width=True)

# ---------------- BACKTEST ----------------
st.subheader("📉 Historical Crash Backtesting")
bt = backtest_crashes(df_i, model, build_features)
st.plotly_chart(backtest_performance(bt), use_container_width=True)

# ---------------- PORTFOLIO STRESS ----------------
st.subheader("💼 Portfolio Stress Test")

portfolio = st.data_editor(
    pd.DataFrame({
        "Firm": df_latest["Firm"].unique(),
        "Weight": [0.0]*len(df_latest)
    }),
    num_rows="dynamic"
)

stress_score, level, detail = portfolio_stress(
    portfolio,
    df_latest[["Firm", "Crash_Probability"]]
)

st.metric("Portfolio Stress Score", round(stress_score,2))
st.write(level)
st.dataframe(detail, use_container_width=True)

