import streamlit as st
import plotly.express as px
import pandas as pd

from engine.data_loader import load_data
from engine.feature_engineering import build_features
from engine.crash_model import train_model, predict
from engine.recommendation_engine import recommend

st.header("Firm Crash Risk Ranking")

st.write(
    "This page identifies which firms are most likely to fail first "
    "during a bubble unwind or market crash."
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

# ---------------- TRAIN MODEL ----------------
model = train_model(df_i, X)

# ---------------- LATEST YEAR ----------------
latest_year = df_i["Year"].max()
latest = df_i[df_i["Year"] == latest_year].copy()

latest["Crash_Probability"] = predict(
    model,
    build_features(latest)
)

latest["Recommendation"] = latest["Crash_Probability"].apply(recommend)

# ---------------- CHART 1: RANKING ----------------
st.subheader("Which Firms Crack First")

st.plotly_chart(
    px.bar(
        latest.sort_values("Crash_Probability"),
        x="Firm",
        y="Crash_Probability",
        title="Firm-Level Crash Probability"
    ),
    use_container_width=True
)

# ---------------- CHART 2: DISTRIBUTION ----------------
st.subheader("Crash Risk Distribution")

st.plotly_chart(
    px.histogram(
        latest,
        x="Crash_Probability",
        nbins=10,
        title="Distribution of Crash Risk"
    ),
    use_container_width=True
)

# ---------------- CHART 3: FRAGILITY MAP ----------------
st.subheader("Financial Fragility Map")

st.plotly_chart(
    px.scatter(
        latest,
        x="Debt_Equity",
        y="Hybrid_EM",
        size="Crash_Probability",
        color="Crash_Probability",
        title="Manipulation vs Leverage"
    ),
    use_container_width=True
)

# ---------------- TABLE ----------------
st.subheader("Detailed Firm Risk Table")

st.dataframe(
    latest.sort_values("Crash_Probability", ascending=False),
    use_container_width=True
)

# ---------------- CONCLUSION ----------------
worst = latest.sort_values(
    "Crash_Probability", ascending=False
).iloc[0]["Firm"]

st.subheader("Conclusion")

st.write(
    "If a crash occurs in this industry, the firm most likely "
    "to fail first based on current indicators is:"
)
st.write(worst)

