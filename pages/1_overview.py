import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from engine.data_loader import load_data

st.header("Market Overview")

file = st.file_uploader("Upload market panel data", type="csv")
df = load_data(file)

df["Year"] = df["Year"].astype(int)
latest_year = df["Year"].max()
latest = df[df["Year"] == latest_year]

# ---------------- KPI TICKER ----------------
st.subheader("Live Market Indicators")

k1, k2, k3, k4 = st.columns(4)

k1.metric("Fragility Index", round(latest["Hybrid_EM"].mean() * 20, 1))
k2.metric("Avg PEG", round(latest["PEG"].mean(), 2))
k3.metric("Avg Leverage", round(latest["Debt_Equity"].mean(), 2))
k4.metric("High Risk Firms %",
          round((latest["Hybrid_EM"] > 2).mean() * 100, 1))

# ---------------- GAUGE ----------------
st.subheader("Systemic Risk Gauge")

gauge = go.Figure(
    go.Indicator(
        mode="gauge+number",
        value=latest["Hybrid_EM"].mean() * 20,
        gauge={
            "axis": {"range": [0, 100]},
            "bar": {"color": "red"},
            "steps": [
                {"range": [0, 30], "color": "green"},
                {"range": [30, 60], "color": "orange"},
                {"range": [60, 100], "color": "darkred"},
            ],
        },
    )
)
st.plotly_chart(gauge, use_container_width=True)

# ---------------- HEATMAP ----------------
st.subheader("Industry Stress Heatmap")

heat = latest.groupby("Industry")[["Hybrid_EM", "PEG", "Debt_Equity"]].mean()

st.plotly_chart(
    px.imshow(heat, color_continuous_scale="Reds", aspect="auto"),
    use_container_width=True
)

# ---------------- TIME SERIES ----------------
st.subheader("Bubble Momentum Over Time")

trend = df.groupby("Year")[["Hybrid_EM", "PEG"]].mean().reset_index()

st.plotly_chart(
    px.line(trend, x="Year", y=["Hybrid_EM", "PEG"]),
    use_container_width=True
)

# ---------------- RANKING ----------------
st.subheader("Top Bubble Industries")

rank = heat.copy()
rank["Score"] = (
    0.4 * rank["Hybrid_EM"]
    + 0.3 * rank["PEG"]
    + 0.3 * rank["Debt_Equity"]
)
rank = rank.sort_values("Score", ascending=False)

st.plotly_chart(
    px.bar(rank.head(6), y="Score"),
    use_container_width=True
)



