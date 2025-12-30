import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from engine.data_loader import load_data

# ---------------- PAGE HEADER ----------------
st.header("Market Fragility Overview")
st.caption(
    "System-level view of bubble risk, valuation stress, "
    "and early warning indicators across industries."
)

# ---------------- DATA LOAD ----------------
uploaded_file = st.file_uploader("Upload market panel data (CSV)", type="csv")
df = load_data(uploaded_file)

df["Year"] = df["Year"].astype(int)

latest_year = int(df["Year"].max())
df_latest = df[df["Year"] == latest_year]

# ---------------- KPI METRICS ----------------
st.subheader("Key Market Indicators")

c1, c2, c3, c4 = st.columns(4)

global_fragility = round(df_latest["Hybrid_EM"].mean() * 20, 1)
avg_peg = round(df_latest["PEG"].mean(), 2)
avg_leverage = round(df_latest["Debt_Equity"].mean(), 2)
high_risk_share = round((df_latest["Hybrid_EM"] > 2.0).mean() * 100, 1)

c1.metric("Global Fragility Index", global_fragility)
c2.metric("Average PEG", avg_peg)
c3.metric("Average Debt/Equity", avg_leverage)
c4.metric("High Risk Firms (%)", f"{high_risk_share}%")

# ---------------- FRAGILITY GAUGE ----------------
st.subheader("Systemic Fragility Gauge")

gauge = go.Figure(
    go.Indicator(
        mode="gauge+number",
        value=global_fragility,
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

# ---------------- INDUSTRY HEATMAP ----------------
st.subheader("Industry Stress Heatmap")

heat = (
    df_latest
    .groupby("Industry")[["Hybrid_EM", "PEG", "Debt_Equity"]]
    .mean()
)

fig_heat = px.imshow(
    heat,
    color_continuous_scale="Reds",
    aspect="auto"
)

st.plotly_chart(fig_heat, use_container_width=True)

# ---------------- TREND ANALYSIS ----------------
st.subheader("Market Bubble Momentum")

trend = (
    df.groupby("Year")[["Hybrid_EM", "PEG"]]
    .mean()
    .reset_index()
)

fig_trend = px.line(
    trend,
    x="Year",
    y=["Hybrid_EM", "PEG"],
    markers=True
)

st.plotly_chart(fig_trend, use_container_width=True)

# ---------------- TOP RISK INDUSTRIES ----------------
st.subheader("Most Stressed Industries")

industry_risk = (
    df_latest
    .groupby("Industry")
    .agg({
        "Hybrid_EM": "mean",
        "PEG": "mean",
        "Debt_Equity": "mean"
    })
    .reset_index()
)

industry_risk["Stress_Score"] = (
    0.4 * industry_risk["Hybrid_EM"]
    + 0.3 * industry_risk["PEG"]
    + 0.3 * industry_risk["Debt_Equity"]
)

industry_risk = industry_risk.sort_values("Stress_Score", ascending=False)

fig_rank = px.bar(
    industry_risk.head(5),
    x="Industry",
    y="Stress_Score"
)

st.plotly_chart(fig_rank, use_container_width=True)

# ---------------- EARLY WARNINGS ----------------
st.subheader("Early Warning Signals")

if global_fragility > 60:
    st.warning("System-wide fragility is elevated.")
if high_risk_share > 35:
    st.warning("High concentration of risky firms detected.")
if industry_risk.iloc[0]["Hybrid_EM"] > 2.0:
    st.warning("Aggressive earnings manipulation observed.")

if global_fragility <= 35:
    st.success("No immediate systemic warning detected.")

# ---------------- FINAL SUMMARY ----------------
st.subheader("Executive Summary")

if global_fragility >= 60:
    st.error(
        "Market conditions indicate late-cycle fragility. "
        "Bubble dynamics are visible across multiple industries."
    )
elif global_fragility >= 35:
    st.warning(
        "Market shows early bubble characteristics. "
        "Risk concentration is rising."
    )
else:
    st.success(
        "Market conditions remain broadly supported. "
        "No systemic bubble detected."
    )

