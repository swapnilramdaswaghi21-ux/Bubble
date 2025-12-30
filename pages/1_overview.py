import streamlit as st
import plotly.express as px
from engine.data_loader import load_data

st.header("🌍 Market Overview")

file = st.file_uploader("Upload Market Data", type="csv")
df = load_data(file)

fragility = df.groupby("Industry")["Hybrid_EM"].mean().reset_index()

st.metric("Global Fragility Index", round(fragility["Hybrid_EM"].mean()*20,1))

st.plotly_chart(
    px.bar(fragility, x="Industry", y="Hybrid_EM",
           title="Industry Bubble Intensity"),
    use_container_width=True
)
