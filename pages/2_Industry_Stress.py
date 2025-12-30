import streamlit as st
import plotly.express as px
from engine.data_loader import load_data

st.header("Industry Stress Dashboard")

file = st.file_uploader("Upload industry data", type="csv")
df = load_data(file)

latest = df[df["Year"] == df["Year"].max()]

industry = latest.groupby("Industry").agg({
    "Hybrid_EM": "mean",
    "PEG": "mean",
    "Debt_Equity": "mean",
    "Return": "mean"
}).reset_index()

st.subheader("Valuation vs Manipulation")

st.plotly_chart(
    px.scatter(
        industry,
        x="PEG",
        y="Hybrid_EM",
        size="Debt_Equity",
        color="Industry"
    ),
    use_container_width=True
)

st.subheader("Leverage Distribution")

st.plotly_chart(
    px.box(latest, x="Industry", y="Debt_Equity"),
    use_container_width=True
)

st.subheader("Industry Returns Under Stress")

st.plotly_chart(
    px.bar(industry, x="Industry", y="Return"),
    use_container_width=True
)
