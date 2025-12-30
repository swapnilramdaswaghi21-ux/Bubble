import streamlit as st
import pandas as pd

st.header("💼 Portfolio Stress Test")

portfolio = st.data_editor(
    pd.DataFrame({"Firm": [], "Weight": []}),
    num_rows="dynamic"
)

st.metric("Portfolio Stress Indicator", "Coming from crash probabilities")
