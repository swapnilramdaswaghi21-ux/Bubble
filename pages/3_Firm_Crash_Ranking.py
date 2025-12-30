import streamlit as st
import plotly.express as px

from engine.data_loader import load_data
from engine.feature_engineering import build_features
from engine.crash_model import train_model, predict
from engine.recommendation_engine import recommend

st.header("Firm Crash Risk Ranking")

st.write(
    "Graphs use multi-year panel data to show broad risk patterns. "
    "The final prediction is based on the most recent year only."
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
X_all = build_features(df_i)

# ---------------- TRAIN MODEL ----------------
model = train_model(df_i, X_all)

# ---------------- MULTI-YEAR DATA (FOR GRAPHS) ----------------
df_i = df_i.copy()
df_i["Crash_Probability"] = predict(model, build_features(df_i))

# ---------------- AGGREGATE RISK ACROSS YEARS ----------------
risk_panel = (
    df_i.groupby("Firm")
    .agg({
        "Crash_Probability": "mean",
        "Hybrid_EM": "mean",
        "PEG": "mean",
        "Debt_Equity": "mean"
    })
    .reset_index()
    .sort_values("Crash_Probability", ascending=False)
)

top10_panel = risk_panel.head(10)

# ---------------- CHART 1: TOP 10 (MULTI-YEAR) ----------------
st.subheader("Top 10 Firms by Average Crash Risk (Panel Data)")

st.plotly_chart(
    px.bar(
        top10_panel[::-1],
        x="Crash_Probability",
        y="Firm",
        orientation="h",
        title="Average Crash Risk Across Years"
    ),
    use_container_width=True
)

# ---------------- CHART 2: FRAGILITY MAP ----------------
st.subheader("Fragility Map (Top 10 Firms)")

st.plotly_chart(
    px.scatter(
        top10_panel,
        x="Debt_Equity",
        y="Hybrid_EM",
        size="Crash_Probability",
        color="Crash_Probability",
        title="Leverage vs Earnings Manipulation"
    ),
    use_container_width=True
)

# ---------------- CHART 3: RISK DISTRIBUTION ----------------
st.subheader("Crash Risk Distribution (All Firms, All Years)")

st.plotly_chart(
    px.histogram(
        df_i,
        x="Crash_Probability",
        nbins=20,
        title="Distribution of Crash Risk"
    ),
    use_container_width=True
)

# ---------------- LATEST YEAR ONLY (FINAL DECISION) ----------------
latest_year = df_i["Year"].max()
latest = df_i[df_i["Year"] == latest_year].copy()

latest["Final_Crash_Probability"] = predict(
    model,
    build_features(latest)
)

latest = latest.sort_values(
    "Final_Crash_Probability", ascending=False
)

latest["Recommendation"] = latest["Final_Crash_Probability"].apply(recommend)

# ---------------- TABLE ----------------
st.subheader("Latest Year Risk Table")

st.dataframe(
    latest[
        [
            "Firm",
            "Final_Crash_Probability",
            "Hybrid_EM",
            "PEG",
            "Debt_Equity",
            "Recommendation"
        ]
    ],
    use_container_width=True
)

# ---------------- FINAL CONCLUSION ----------------
worst_firm = latest.iloc[0]["Firm"]

st.subheader("Final Prediction")

st.write(
    "Based on the most recent financial data, the firm most likely "
    "to fail first in the event of a crash is:"
)
st.write(worst_firm)



