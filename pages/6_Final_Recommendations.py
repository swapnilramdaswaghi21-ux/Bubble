import streamlit as st
from engine.data_loader import load_data

st.header("Final Risk Assessment")

df = load_data()

rank = (
    df.groupby("Firm")["Hybrid_EM"]
    .mean()
    .sort_values(ascending=False)
)

st.subheader("Firms Most Vulnerable in a Crash")

for firm in rank.head(5).index:
    st.write(firm)

st.subheader("Recommended Actions")

st.write("Reduce exposure to top ranked firms.")
st.write("Increase hedging in high risk industries.")
st.write("Avoid new investments in late cycle sectors.")

