import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from engine.data_loader import load_data

# ---------------- PAGE HEADER ----------------
st.header("🌍 Market Fragility Overview")
st.caption(
    "High-level diagnostic of market stress, bubble intensity, "
    "and early-warning signals across industries."
)

# ---------------- DATA LOAD ----------------
file = st.file_uploader("Upload Market Panel Data (CSV)", type="csv")
df = load_data(file)

# Ensure correct types
df["Year"] = df["Year"].astype(int)

latest_year = df["Year"].max()
df_latest = df[df["Year"] == latest_year]

# ---------------- KPI / TICKER ROW ----------------
st.subheader("📊 Key Market Indicators")

col1, col2, col3, col4 = st.columns(4)

global_fragility = round(df_latest["Hybrid_EM"].mean() * 20, 1)
avg_valuation = round(df_latest["PEG"].mean(), 2)
avg_leverage = round(df_latest["Debt_Equity"].mean(), 2)
high_risk_share = round((df_latest["Hybrid_EM"] > 2.0).mean() * 100, 1)

col1.metric("Global Fragility Index", global_fragility)
col2.metric("Avg Market PEG", avg_valuation)
col3.metric("Avg Debt / Equity", avg_leverage)
col4.metric("High-Risk Firms (%)", f"{high_risk_share}%")

# ---------------- FRAGILITY GAUGE ----------------
st.subheader("🚨 Market Fragility Gauge")

gauge = go.Figure(go.Indicator(
    mode="gauge+number",
    value=global_fragility,
    title={"text": "Systemic Market Fragility"},
    gauge={
        "axis": {"range": [0, 100]},
        "bar": {"color": "#ef4444"},
        "steps": [
            {"range": [0, 30], "color": "#064e3b"},
            {"range": [30, 60], "color": "#92400e"},
            {"range": [60, 100], "color": "#7f1d1d"},
        ],
    },
))
st.plotly_chart(gauge, use_container_width=True)

# ---------------- INDUSTRY HEATMAP ----------------
st.subheader("🔥 Industry Bubble Heatmap (Latest Year)")

heatmap_data = (
    df_latest
    .groupby("Industry")[["Hybrid_EM", "PEG", "Debt_Equity"]]
    .mean()
    .reset_index()
)

fig_heat = px.imshow(
    heatmap_data.set_index("Industry"),
    color_continuous_scale="Reds",
    aspect="auto",
    title="Industry-Level Bubble Stress (Manipulation × Valuation × Leverage)"
)

st.plotly_chart(fig_heat, use_container_width=True)

# ---------------- BUBBLE MOMENTUM TREND ----------------
st.subheader("📈 Bubble Momentum Trend (Market-Wide)")

trend = (
    df.groupby("Year")[["Hybrid_EM", "PEG"]]
    .mean()
    .reset_index()
)

st.plotly_chart(
    px.line(
        trend,
        x="Year",
        y=["Hybrid_EM", "PEG"],
        markers=True,
        title="Earnings Manipulation vs Valuation Over Time"
    ),
    use_container_width=True
)

# ---------------- TOP STRESSED INDUSTRIES ----------------
st.subheader("🏭 Top Bubble-Prone Industries")

industry_rank = (
    df_latest
    .groupby("Industry")
    .agg({
        "Hybrid_EM": "mean",
        "PEG": "mean",
        "Debt_Equity": "mean"
    })
    .reset_index()
)

industry_rank["Stress_Score"] = (
    0.4 * industry_rank["Hybrid_EM"] +
    0.3 * industry_rank["PEG"] +
    0.3 * industry_rank["Debt_Equity"]
)

industry_rank = industry_rank.sort_values("Stress_Score", ascending=False)

st.plotly_chart(
    px.bar(
        industry_rank.head(5),
        x="Industry",
        y="Stress_Score",
        title="Industries Most Exposed to Bubble Risk"
    ),
    use_container_width=True
)

# ---------------- EARLY WARNING SIGNALS ----------------
st.subheader("⚠️ Early Warning Signals")

signals = []

if global_fragility > 60:
    signals.append("System-wide fragility elevated")
if high_risk_share > 35:
    signals.append("Large concentration of high-risk firms")
if industry_rank.iloc[0]["Hybrid_EM"] > 2.0:
    signals.append("Aggressive earnings manipulation detected")

if signals:
    for s in signals:
        st.warning(s)
else:
    st.success("No immediate systemic warning signals detected")

# ---------------- EXECUTIVE CONCLUSION ----------------
st.subheader("📌 Executive Summary")

if global_fragility >= 60:
    st.error(
        "Market conditions indicate **late-cycle fragility**. "
        "Bubble dynamics are present across multiple industries. "
        "Downside risk is asymmetric."
    )
elif global_fragility >= 35:
    st.warning(
        "Market shows **early-to-mid bubble characteristics**. "
        "Risk concentration is rising. Close monitoring advised."
    )
else:
    st.success(
        "Market conditions remain **fundamentally supported**. "
        "No broad-based bubble detected at this stage."
    )

st.caption(
    "This overview aggregates firm-level signals into a "
    "systemic market risk diagnostic used for early-warning and "
    "strategic alloc

