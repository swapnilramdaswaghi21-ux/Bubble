import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from engine.data_loader import load_data

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.header("Industry Stress Dashboard")

st.write(
    "This page evaluates systemic stress across industries using "
    "earnings manipulation, valuation excess, leverage, and return compression."
)

# -------------------------------------------------
# LOAD DATA
# -------------------------------------------------
file = st.file_uploader("Upload industry-level panel data", type="csv")
df = load_data(file)

df["Year"] = df["Year"].astype(int)

latest_year = df["Year"].max()
latest = df[df["Year"] == latest_year]

# -------------------------------------------------
# KPI STRIP
# -------------------------------------------------
st.subheader("Market-Wide Stress Indicators")

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Avg Hybrid EM",
    round(latest["Hybrid_EM"].mean(), 2)
)

c2.metric(
    "Avg PEG",
    round(latest["PEG"].mean(), 2)
)

c3.metric(
    "Avg Debt Equity",
    round(latest["Debt_Equity"].mean(), 2)
)

c4.metric(
    "Industries in Distress (%)",
    round((latest["Return"] < -0.30).mean() * 100, 1)
)

# -------------------------------------------------
# AGGREGATE INDUSTRY STRESS
# -------------------------------------------------
industry_panel = (
    df.groupby(["Industry", "Year"])
    .agg({
        "Hybrid_EM": "mean",
        "PEG": "mean",
        "Debt_Equity": "mean",
        "Return": "mean"
    })
    .reset_index()
)

latest_industry = industry_panel[
    industry_panel["Year"] == latest_year
].copy()

latest_industry["Stress_Score"] = (
    0.4 * latest_industry["Hybrid_EM"]
    + 0.3 * latest_industry["PEG"]
    + 0.3 * latest_industry["Debt_Equity"]
)

# -------------------------------------------------
# CHART 1: INDUSTRY STRESS RANKING
# -------------------------------------------------
st.subheader("Industry Bubble Stress Ranking")

st.plotly_chart(
    px.bar(
        latest_industry.sort_values("Stress_Score"),
        x="Stress_Score",
        y="Industry",
        orientation="h",
        title="Composite Industry Stress Score"
    ),
    use_container_width=True
)

# -------------------------------------------------
# CHART 2: VALUATION VS MANIPULATION MAP
# -------------------------------------------------
st.subheader("Valuation Excess vs Earnings Manipulation")

st.plotly_chart(
    px.scatter(
        latest_industry,
        x="PEG",
        y="Hybrid_EM",
        size="Debt_Equity",
        color="Stress_Score",
        title="Bubble Formation Map by Industry"
    ),
    use_container_width=True
)

# -------------------------------------------------
# CHART 3: LEVERAGE DISTRIBUTION
# -------------------------------------------------
st.subheader("Industry Leverage Distribution")

st.plotly_chart(
    px.box(
        latest,
        x="Industry",
        y="Debt_Equity",
        title="Leverage Dispersion Across Industries"
    ),
    use_container_width=True
)

# -------------------------------------------------
# CHART 4: STRESS EVOLUTION OVER TIME
# -------------------------------------------------
st.subheader("Stress Evolution Over Time")

stress_trend = (
    industry_panel
    .groupby("Year")[["Hybrid_EM", "PEG", "Debt_Equity"]]
    .mean()
    .reset_index()
)

st.plotly_chart(
    px.line(
        stress_trend,
        x="Year",
        y=["Hybrid_EM", "PEG", "Debt_Equity"],
        title="Systemic Stress Indicators Over Time"
    ),
    use_container_width=True
)

# -------------------------------------------------
# CHART 5: RETURN COMPRESSION
# -------------------------------------------------
st.subheader("Return Compression Under Stress")

st.plotly_chart(
    px.scatter(
        latest_industry,
        x="Stress_Score",
        y="Return",
        title="Higher Stress Leads to Sharper Downside"
    ),
    use_container_width=True
)

# -------------------------------------------------
# HEATMAP: MULTI-DIMENSIONAL STRESS
# -------------------------------------------------
st.subheader("Multi-Dimensional Industry Stress Heatmap")

heatmap_data = (
    latest_industry
    .set_index("Industry")[["Hybrid_EM", "PEG", "Debt_Equity", "Return"]]
)

st.plotly_chart(
    px.imshow(
        heatmap_data,
        color_continuous_scale="Reds",
        aspect="auto"
    ),
    use_container_width=True
)

# -------------------------------------------------
# CONCLUSION
# -------------------------------------------------
most_stressed = latest_industry.sort_values(
    "Stress_Score", ascending=False
).iloc[0]["Industry"]

st.subheader("Conclusion")

st.write(
    "Based on current fundamentals, the industry exhibiting "
    "the highest bubble and crash risk is:"
)
st.write(most_stressed)




