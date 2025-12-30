import streamlit as st

st.header("⚠️ Scenario Simulator")

shock = st.selectbox(
    "Select Market Shock",
    ["Mild Correction (-10%)", "Severe Crash (-30%)", "Liquidity Shock"]
)

st.write(f"Simulating impact under **{shock}** conditions.")
