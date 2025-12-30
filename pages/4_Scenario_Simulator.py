import streamlit as st
import plotly.express as px
from engine.data_loader import load_data

st.header("Market Scenario Simulator")

file = st.file_uploader("Upload scenario data", type="csv")
df = load_data(file)

scenario = st.selectbox(
    "Scenario",
    ["Mild Correction", "Severe Crash", "Liquidity Shock"]
)

factor = {"Mild Correction": 0.1, "Severe Crash": 0.3, "Liquidity Shock": 0.4}[scenario]
df["Impact"] = df["Debt_Equity"] * factor

st.plotly_chart(
    px.histogram(df, x="Impact"),
    use_container_width=True
)

st.plotly_chart(
    px.box(df, y="Impact"),
    use_container_width=True
)
