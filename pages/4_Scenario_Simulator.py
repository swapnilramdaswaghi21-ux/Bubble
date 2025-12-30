import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

from engine.data_loader import load_data
from engine.feature_engineering import build_features
from engine.crash_model import train_model, predict

# -------------------------------------------------
# PAGE HEADER
# -------------------------------------------------
st.header("Scenario Simulator")

st.write(
    "Simulate how different market crash scenarios impact industries "
    "and identify which firms are most likely to fail first."
)

# -------------------------------------------------
# LOAD DATA
# -------------------------------------------------
file = st.file_uploader("Upload firm-level panel data", type="csv")
df = load_data(file)

df["Year"] = df["Year"].astype(int)
latest_year = df["Year"].max()
latest = df[df["Year"] == latest_year]

# -------------------------------------------------
# SCENARIO SELECTION
# -------------------------------------------------
st.subheader("Select Crisis Scenario")

scenario = st.selectbox(
    "Market Stress Scenario",
    [
        "Mild Correction (Valuation Reset)",
        "Severe Market Crash (Leverage Unwind)",
        "Liquidity Freeze (2008-style)",
        "Sector Bubble Burst"
    ]
)

# -------------------------------------------------
# SCENARIO PARAMETERS
# -------------------------------------------------
if scenario == "Mild Correction (Valuation Reset)":
    shock_val = 0.10
    shock_lev = 0.05
    shock_liq = 0.00

elif scenario == "Severe Market Crash (Leverage Unwind)":
    shock_val = 0.25
    shock_lev = 0.20
    shock_liq = 0.10

elif scenario == "Liquidity Freeze (2008-style)":
    shock_val = 0.30
    shock_lev = 0.30
    shock_liq = 0.25

else:  # Sector Bubble Burst
    shock_val = 0.35
    shock_lev = 0.15
    shock_liq = 0.10

# -------------------------------------------------
# APPLY SHOCKS
# -------------------------------------------------
sim = latest.copy()

sim["Valuation_Shock"] = sim["PEG"] * shock_val
sim["Leverage_Shock"] = sim["Debt_Equity"] * shock_lev
sim["Liquidity_Shock"] = (-sim["CFO_Growth"]) * shock_liq

sim["Total_Stress"] = (
    sim["Valuation_Shock"]
    + sim["Leverage_Shock"]
    + sim["Liquidity_Shock"]
)

# -------------------------------------------------
# ML CRASH PROBABILITY
# -------------------------------------------------
X = build_features(df)
model = train_model(df, X)

sim["Crash_Probability"] = predict(
    model,
    build_features(sim)
)

# -------------------------------------------------
# KPI STRIP
# -------------------------------------------------
st.subheader("System Impact Summary")

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Avg Crash Probability",
    round(sim["Crash_Probability"].mean(), 2)
)

c2.metric(
    "High Risk Firms (%)",
    round((sim["Crash_Probability"] > 0.6).mean() * 100, 1)
)

c3.metric(
    "Industries Affected",
    sim["Industry"].nunique()
)

c4.metric(
    "Worst Impact Firm",
    sim.sort_values("Crash_Probability", ascending=False).iloc[0]["Firm"]
)

# -------------------------------------------------
# CHART 1: INDUSTRY DAMAGE
# -------------------------------------------------
st.subheader("Industry-Level Stress Under Scenario")

industry_damage = (
    sim.groupby("Industry")["Total_Stress"]
    .mean()
    .reset_index()
)

st.plotly_chart(
    px.bar(
        industry_damage.sort_values("Total_Stress"),
        x="Total_Stress",
        y="Industry",
        orientation="h",
        title="Average Stress by Industry"
    ),
    use_container_width=True
)

# -------------------------------------------------
# CHART 2: FIRMS MOST LIKELY TO FAIL
# -------------------------------------------------
st.subheader("Firms Most Likely to Fail First")

top_failures = (
    sim.sort_values("Crash_Probability", ascending=False)
    .head(10)
)

st.plotly_chart(
    px.bar(
        top_failures[::-1],
        x="Crash_Probability",
        y="Firm",
        orientation="h",
        title="Top 10 Firms by Crash Probability"
    ),
    use_container_width=True
)

# -------------------------------------------------
# CHART 3: STRESS MAP
# -------------------------------------------------
st.subheader("Stress Transmission Map")

st.plotly_chart(
    px.scatter(
        sim,
        x="Debt_Equity",
        y="PEG",
        size="Crash_Probability",
        color="Industry",
        title="Leverage vs Valuation Under Stress"
    ),
    use_container_width=True
)

# -------------------------------------------------
# CHART 4: DISTRIBUTION
# -------------------------------------------------
st.subheader("Crash Probability Distribution")

st.plotly_chart(
    px.histogram(
        sim,
        x="Crash_Probability",
        nbins=20,
        title="Distribution of Firm-Level Crash Risk"
    ),
    use_container_width=True
)

# -------------------------------------------------
# DECISION TABLE
# -------------------------------------------------
st.subheader("Actionable Firm-Level Decisions")

st.dataframe(
    top_failures[
        [
            "Firm",
            "Industry",
            "Crash_Probability",
            "Total_Stress",
            "Debt_Equity",
            "PEG"
        ]
    ],
    use_container_width=True
)

# -------------------------------------------------
# FINAL RECOMMENDATION
# -------------------------------------------------
worst = top_failures.iloc[0]["Firm"]

st.subheader("Scenario Recommendation")

st.write(
    "Under the selected scenario, the firm most likely to fail first is:"
)
st.write(worst)

st.write(
    "Recommended actions:"
)
st.write("- Reduce or exit exposure to high crash probability firms")
st.write("- Increase hedging in affected industries")
st.write("- Avoid leveraged firms with weak cash flows")
