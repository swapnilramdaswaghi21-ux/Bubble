import streamlit as st
import pandas as pd
import plotly.express as px

st.header("Portfolio Stress Test")

portfolio = st.data_editor(
    pd.DataFrame({"Firm": [], "Weight": []}),
    num_rows="dynamic"
)

if not portfolio.empty:
    portfolio["Weighted_Risk"] = portfolio["Weight"]
    st.plotly_chart(
        px.pie(portfolio, names="Firm", values="Weighted_Risk"),
        use_container_width=True
    )
