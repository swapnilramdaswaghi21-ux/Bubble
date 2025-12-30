import streamlit as st
import plotly.express as px

from engine.data_loader import load_data
from engine.feature_engineering import build_features
from engine.crash_model import train_model, predict
from engine.recommendation_engine import recommend

st.header("Firm Crash Risk Ranking")

st.write(
    "This page ranks firms within an industry by their likelihood "
    "of failing first during a market crash or bubble unwind."
)

# ---------------- LOAD DATA ----------------
file = st.file_uploader("Upload firm-level panel data", type="csv")
df = load_data(file)

df["Year"] = df["Year"].astype(int)

# ---------------- SELECT INDUSTRY ----------------
industry = st.selectbox(
    "Select Industry",
    sorted(df["Industry"].unique())
)

df_i = df[df["Industry"] == industry]

# ---------------- FEATURE ENGINEERING ----------------
X = build_features(df_i)

# ---------------- TRAIN MODEL (SAFE) ----------------
model = train_model(df_i, X)

# ---------------- USE LATEST YEAR ----------------
latest_year = df_i["Year"].max()
latest = df_i[df_i["Year"] == latest_year].copy()

latest["Crash_Probability"] = predict(
    model,
    build_features(latest)
)

latest["Recommendation"] = latest["Crash_Probability"].apply(recommend)

# ---------------- SORT & SELECT TOP 10 ----------------
latest_sorted = latest.sort_values(
    "Crash_Probability", ascending=False
)

top10 = latest_sorted.head(10)

# ---------------- CHART 1: TOP 10 RANKING ----------------
st.subheader("Top 10 Firms Most Likely to Crash First")

st.plotly_chart(
    px.bar(
        top10[::-1],
        x="Crash_Probability",
        y="Firm",
        orientation="h",
        title="Top 10 Crash Risk Ranking"
    ),
    use_container_width=True
)

# ---------------- CHART 2: FRAGILITY MAP (TOP 10) ----------------
st.subheader("Fragility Map of Top 10 Firms")

st.plotly_chart(
    px.scatter(
        top10,
        x="Debt_Equity",
        y="Hybrid_EM",
        size="Crash_Probability",
        color="Crash_Probability",
        title="Leverage vs Earnings Manipulation (Top 10)"
    ),
    use_container_width=True
)

# ---------------- CHART 3: FULL DISTRIBUTION ----------------
st.subheader("Crash Risk Distribution (All Firms in Industry)")

st.plotly_chart(
    px.histogram(
        latest_sorted,
        x="Crash_Probability",
        nbins=15,
        title="Distribution of Crash Risk"
    ),
    use_container_width=True
)

# ---------------- TABLE: TOP 10 ----------------
st.subheader("Top 10 Firm Risk Table")

st.dataframe(
    top10[
        [
            "Firm",
            "Crash_Probability",
            "Hybrid_EM",
            "PEG",
            "Debt_Equity",
            "Recommendation",
        ]
    ],
    use_container_width=True
)

# ---------------- CONCLUSION ----------------
worst_firm = top10.iloc[0]["Firm"]

st.subheader("Conclusion")

st.write(
    "Based on current financial fragility indicators, "
    "the firm most likely to fail first in this industry is:"
)
st.write(worst_firm)

st.write(
    "The remaining firms in the Top 10 also exhibit elevated "
    "risk and should be closely monitored during market stress."
)


