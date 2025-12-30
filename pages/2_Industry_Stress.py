import streamlit as st
from engine.data_loader import load_data

df = load_data()

st.header("🏭 Industry Stress Monitor")

stress = (
    df.groupby("Industry")
    .agg({
        "Hybrid_EM": "mean",
        "PEG": "mean",
        "Debt_Equity": "mean"
    })
)

st.dataframe(stress, use_container_width=True)
