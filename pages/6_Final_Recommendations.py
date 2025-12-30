import streamlit as st
import pandas as pd
import plotly.express as px

from engine.data_loader import load_data
from engine.feature_engineering import build_features
from engine.crash_model import train_model, predict
from engine.recommendation_engine import recommend

# -------------------------------------------------
# PAGE HEADER
# -------------------------------------------------
st.header("Final Risk Assessment and Strategic Actions")

st.write(
    "This page consolidates market, industry, firm, scenario, "
    "and portfolio insights into clear, high-confidence decisions "
    "suitable for investment committees and risk teams."
)

# -------------------------------------------------
# LOAD DATA
# -------------------------------------------------
file = st.file_uploader(
    "Upload firm-level panel data (CSV)",
    type="csv"
)

df = load_data(file)
df["Year"] = df["Year"].astype(int)

latest_year = df["Year"].max()
latest = df[df["Year"] == latest_year]

# -------------------------------------------------
# TRAIN CRASH MODEL (GLOBAL)
# -------------------------------------------------
X_all = build_features(df)
model = train_model(df, X_all)

latest["Crash_Probability"] = predict(
    model,
    build_features(latest)
)

latest["Recommendation"] = latest["Crash_Probability"].apply(recommend)

# -------------------------------------------------
# SYSTEM LEVEL METRICS
# -------------------------------------------------
st.subheader("System-Wide Risk Summary")

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Average Crash Probability",
    round(latest["Crash_Probability"].mean(), 2)
)

c2.metric(
    "High Risk Firms (%)",
    round((latest["Crash_Probability"] > 0.6).mean() * 100, 1)
)

c3.metric(
    "Industries at Risk",
    latest["Industry"].nunique()
)

c4.metric(
    "Worst Firm Identified",
    latest.sort_values(
        "Crash_Probability", ascending=False
    ).iloc[0]["Firm"]
)

# -------------------------------------------------
# TOP FIRMS TO ACT ON
# -------------------------------------------------
st.subheader("Top Firms Requiring Immediate Action")

top_firms = (
    latest.sort_values("Crash_Probability", ascending=False)
    .head(10)
)

st.plotly_chart(
    px.bar(
        top_firms[::-1],
        x="Crash_Probability",
        y="Firm",
        orientation="h",
        title="Top 10 Firms by Crash Probability"
    ),
    use_container_width=True
)

st.dataframe(
    top_firms[
        [
            "Firm",
            "Industry",
            "Crash_Probability",
            "Hybrid_EM",
            "PEG",
            "Debt_Equity",
            "Recommendation"
        ]
    ],
    use_container_width=True
)

# -------------------------------------------------
# INDUSTRY ACTION MAP
# -------------------------------------------------
st.subheader("Industry-Level Strategic Posture")

industry_actions = (
    latest.groupby("Industry")
    .agg({
        "Crash_Probability": "mean",
        "Hybrid_EM": "mean",
        "Debt_Equity": "mean"
    })
    .reset_index()
)

industry_actions["Industry_Action"] = industry_actions[
    "Crash_Probability"
].apply(
    lambda x: "Reduce Exposure" if x > 0.6 else
              "Hedge Selectively" if x > 0.4 else
              "Maintain Exposure"
)

st.plotly_chart(
    px.scatter(
        industry_actions,
        x="Debt_Equity",
        y="Hybrid_EM",
        size="Crash_Probability",
        color="Industry_Action",
        title="Industry Risk Posture Map"
    ),
    use_container_width=True
)

st.dataframe(
    industry_actions[
        [
            "Industry",
            "Crash_Probability",
            "Industry_Action"
        ]
    ],
    use_container_width=True
)

# -------------------------------------------------
# HIGH VALUE STRATEGIC OPTIONS
# -------------------------------------------------
st.subheader("High-Value Strategic Options")

st.markdown("Recommended actions by risk tier:")

st.write("1. Immediate Exit Candidates")
exit_firms = top_firms[
    top_firms["Crash_Probability"] > 0.75
]["Firm"].tolist()
if exit_firms:
    for f in exit_firms:
        st.write("- " + f)
else:
    st.write("- None identified")

st.write("2. Hedge or Reduce Exposure")
hedge_firms = top_firms[
    (top_firms["Crash_Probability"] <= 0.75) &
    (top_firms["Crash_Probability"] > 0.50)
]["Firm"].tolist()
if hedge_firms:
    for f in hedge_firms:
        st.write("- " + f)
else:
    st.write("- None identified")

st.write("3. Monitor Closely")
monitor_firms = top_firms[
    top_firms["Crash_Probability"] <= 0.50
]["Firm"].tolist()
if monitor_firms:
    for f in monitor_firms:
        st.write("- " + f)
else:
    st.write("- None identified")

# -------------------------------------------------
# FINAL VERDICT
# -------------------------------------------------
worst_firm = top_firms.iloc[0]["Firm"]
worst_industry = top_firms.iloc[0]["Industry"]

st.subheader("Final Verdict")

st.write(
    "Based on the integrated analysis across accounting quality, "
    "valuation excess, leverage, scenario stress, and portfolio impact:"
)

st.write(
    "The firm most likely to fail first in a market crash is:"
)
st.write(worst_firm)

st.write(
    "The industry requiring the most immediate risk reduction is:"
)
st.write(worst_industry)

st.write(
    "Recommended next steps:"
)
st.write("- Reduce or exit exposure to the identified firm")
st.write("- Increase hedging in the identified industry")
st.write("- Avoid new late-cycle investments in high-risk sectors")
st.write("- Reassess portfolio concentration monthly")
