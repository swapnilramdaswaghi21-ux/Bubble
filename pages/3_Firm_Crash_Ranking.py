import streamlit as st
import plotly.express as px
from engine.data_loader import load_data
from engine.feature_engineering import build_features
from engine.crash_model import train_model, predict
from engine.recommendation_engine import recommend

st.header("🚨 Firms Likely to Crash First")

file = st.file_uploader("Upload Firm Data", type="csv")
df = load_data(file)

industry = st.selectbox("Select Industry", df["Industry"].unique())
df_i = df[df["Industry"] == industry]

X = build_features(df_i)
model = train_model(df_i, X)

latest = df_i[df_i["Year"] == df_i["Year"].max()].copy()
latest["Crash_Probability"] = predict(model, build_features(latest))
latest["Recommendation"] = latest["Crash_Probability"].apply(recommend)

st.plotly_chart(
    px.bar(latest.sort_values("Crash_Probability"),
           x="Firm", y="Crash_Probability",
           title="Crash Probability Ranking"),
    use_container_width=True
)

st.dataframe(
    latest.sort_values("Crash_Probability", ascending=False)[
        ["Firm","Crash_Probability","Recommendation"]
    ],
    use_container_width=True
)

