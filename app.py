import streamlit as st
import pandas as pd
from utils.bubble_logic import compute_bubble_score
from utils.charts import bubble_gauge, driver_bar

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="AI Industry Bubble Detector",
    page_icon="🧠",
    layout="wide"
)

# Load CSS
with open("assets/styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("<h1 class='title'>AI Industry Bubble Recognition System</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Earnings Manipulation × Valuation × Explainable AI</p>", unsafe_allow_html=True)

# ---------------- LOAD DATA ----------------
df = pd.read_csv("data/sample_ai_industry.csv")

# ---------------- COMPUTE ----------------
bubble_score, metrics, verdict = compute_bubble_score(df)

# ---------------- TOP METRICS ----------------
c1, c2, c3 = st.columns(3)

c1.metric("Bubble Risk Score", f"{bubble_score}/100")
c2.metric("High EM Firms", f"{metrics['high_em_pct']}%")
c3.metric("Avg PEG Ratio", metrics["avg_peg"])

# ---------------- GAUGE ----------------
st.plotly_chart(bubble_gauge(bubble_score), use_container_width=True)

# ---------------- TABLE ----------------
st.subheader("Firm-Level Diagnostics")
st.dataframe(df, use_container_width=True)

# ---------------- DRIVERS ----------------
st.subheader("Key Bubble Drivers")
st.plotly_chart(driver_bar(), use_container_width=True)

# ---------------- CONCLUSION ----------------
st.subheader("Final Verdict")

if verdict:
    st.markdown(
        "<div class='verdict bad'>🚨 BUBBLE DETECTED<br>"
        "Aggressive earnings manipulation and valuation excess observed.<br>"
        "<b>High-risk firms:</b> NVIDIA, Palantir</div>",
        unsafe_allow_html=True
    )
else:
    st.markdown(
        "<div class='verdict good'>✅ NO SYSTEMIC BUBBLE DETECTED</div>",
        unsafe_allow_html=True
    )
