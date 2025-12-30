import streamlit as st
import pandas as pd
import plotly.express as px

from engine.data_loader import load_data
from engine.feature_engineering import build_features
from engine.crash_model import train_model, predict

# -------------------------------------------------
# PAGE HEADER
# -------------------------------------------------
st.header("Portfolio Impact Analysis")

st.write(
    "Evaluate how a market crash or bubble unwind impacts a portfolio. "
    "This page identifies concentration risk, expected drawdowns, "
    "and the firms contributing most to portfolio stress."
)

# -------------------------------------------------
# LOAD MARKET DATA (FOR RISK ESTIMATION)
# -------------------------------------------------
file_market = st.file_uploader(
    "Upload firm-level market data (CSV)",
    type="csv",
    key="market"
)
market_df = load_data(file_market)

market_df["Year"] = market_df["Year"].astype(int)
latest_year = market_df["Year"].max()
latest_market = market_df[market_df["Year"] == latest_year]

# -------------------------------------------------
# SAMPLE PORTFOLIO DATA (AUTO-LOADED)
# -------------------------------------------------
st.subheader("Portfolio Holdings")

st.caption(
    "An example portfolio is preloaded. "
    "You can edit weights or upload your own portfolio CSV."
)

sample_portfolio = pd.DataFrame({
    "Firm": [
        "LehmanBrothers",
        "Citigroup",
        "GoldmanSachs",
        "JPmorgan",
        "MorganStanley",
        "BankOfAmerica"
    ],
    "Weight": [0.20, 0.18, 0.17, 0.15, 0.15, 0.15]
})

file_portfolio = st.file_uploader(
    "Upload portfolio file (Firm, Weight)",
    type="csv",
    key="portfolio"
)

if file_portfolio is not None:
    portfolio = pd.read_csv(file_portfolio)
else:
    portfolio = sample_portfolio.copy()

portfolio = st.data_editor(
    portfolio,
    num_rows="dynamic",
    use_container_width=True
)

# -------------------------------------------------
# MERGE PORTFOLIO WITH MARKET DATA
# -------------------------------------------------
merged = portfolio.merge(
    latest_market,
    on="Firm",
    how="left"
)

merged = merged.dropna(subset=["Hybrid_EM", "PEG", "Debt_Equity"])

# -------------------------------------------------
# TRAIN CRASH MODEL
# -------------------------------------------------
X_all = build_features(market_df)
model = train_model(market_df, X_all)

merged["Crash_Probability"] = predict(
    model,
    build_features(merged)
)

# -------------------------------------------------
# PORTFOLIO RISK METRICS
# -------------------------------------------------
merged["Weighted_Risk"] = merged["Weight"] * merged["Crash_Probability"]

portfolio_crash_risk = merged["Weighted_Risk"].sum()

expected_drawdown = (
    merged["Weight"] * merged["Crash_Probability"] * 0.40
).sum()

# -------------------------------------------------
# KPI STRIP
# -------------------------------------------------
st.subheader("Portfolio Risk Summary")

c1, c2, c3 = st.columns(3)

c1.metric(
    "Portfolio Crash Risk",
    round(portfolio_crash_risk, 2)
)

c2.metric(
    "Expected Drawdown",
    f"{round(expected_drawdown * 100, 1)} %"
)

c3.metric(
    "High Risk Exposure (%)",
    round(
        (merged["Crash_Probability"] > 0.6).mean() * 100,
        1
    )
)

# -------------------------------------------------
# CHART 1: CONTRIBUTION TO RISK
# -------------------------------------------------
st.subheader("Contribution to Portfolio Risk")

st.plotly_chart(
    px.bar(
        merged.sort_values("Weighted_Risk"),
        x="Weighted_Risk",
        y="Firm",
        orientation="h",
        title="Which Holdings Drive Portfolio Stress"
    ),
    use_container_width=True
)

# -------------------------------------------------
# CHART 2: WEIGHT VS RISK MAP
# -------------------------------------------------
st.subheader("Weight vs Crash Probability")

st.plotly_chart(
    px.scatter(
        merged,
        x="Weight",
        y="Crash_Probability",
        size="Weighted_Risk",
        color="Firm",
        title="Concentration and Crash Exposure"
    ),
    use_container_width=True
)

# -------------------------------------------------
# CHART 3: PORTFOLIO COMPOSITION
# -------------------------------------------------
st.subheader("Portfolio Composition")

st.plotly_chart(
    px.pie(
        merged,
        names="Firm",
        values="Weight",
        title="Portfolio Weights"
    ),
    use_container_width=True
)

# -------------------------------------------------
# DETAILED TABLE
# -------------------------------------------------
st.subheader("Detailed Portfolio Risk Table")

st.dataframe(
    merged[
        [
            "Firm",
            "Weight",
            "Crash_Probability",
            "Weighted_Risk",
            "Hybrid_EM",
            "PEG",
            "Debt_Equity"
        ]
    ].sort_values("Weighted_Risk", ascending=False),
    use_container_width=True
)

# -------------------------------------------------
# FINAL RECOMMENDATION
# -------------------------------------------------
worst_firm = (
    merged.sort_values("Weighted_Risk", ascending=False)
    .iloc[0]["Firm"]
)

st.subheader("Portfolio Recommendation")

st.write(
    "The largest contributor to portfolio crash risk is:"
)
st.write(worst_firm)

st.write(
    "Recommended actions:"
)
st.write("- Reduce exposure to high-risk holdings")
st.write("- Rebalance away from leveraged firms")
st.write("- Increase diversification across industries")

