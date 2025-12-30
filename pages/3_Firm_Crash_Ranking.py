import streamlit as st
from engine.data_loader import load_data
from engine.feature_engineering import build_features
from engine.crash_model import train_model, predict_probabilities
from engine.recommendation_engine import recommend

df = load_data()
industry = st.selectbox("Select Industry", df["Industry"].unique())
df_i = df[df["Industry"] == industry]

X = build_features(df_i)
model = train_model(df_i, X)

df_latest = df_i[df_i["Year"] == df_i["Year"].max()].copy()
df_latest["Crash_Probability"] = predict_probabilities(
    model,
    build_features(df_latest)
)

df_latest["Recommendation"] = df_latest["Crash_Probability"].apply(recommend)

st.header("🚨 Firms Most Likely to Crash First")
st.dataframe(
    df_latest.sort_values("Crash_Probability", ascending=False)[
        ["Firm", "Crash_Probability", "Recommendation"]
    ],
    use_container_width=True
)
