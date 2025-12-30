import streamlit as st
import plotly.express as px
from engine.data_loader import load_data
from engine.feature_engineering import build_features
from engine.crash_model import train_model, predict
from engine.recommendation_engine import recommend

st.header("Firm Crash Risk Ranking")

file = st.file_uploader("Upload firm data", type="csv")
df = load_data(file)

industry = st.selectbox("Select industry", df["Industry"].unique())
df_i = df[df["Industry"] == industry]

X = build_features(df_i)
model = train_model(df_i, X)

latest = df_i[df_i["Year"] == df_i["Year"].max()].copy()
latest["Crash_Probability"] = predict(model, build_features(latest))
latest["Recommendation"] = latest["Crash_Probability"].apply(recommend)

st.subheader("Crash Probability Ranking")

st.plotly_chart(
    px.bar(
        latest.sort_values("Crash_Probability"),
        x="Firm",
        y="Crash_Probability"
    ),
    use_container_width=True
)

st.subheader("Risk Distribution")

st.plotly_chart(
    px.histogram(latest, x="Crash_Probability"),
    use_container_width=True
)

st.subheader("Detailed Firm Table")

st.dataframe(latest, use_container_width=True)
