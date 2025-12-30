import streamlit as st
import pandas as pd
import os

from utils.bubble_logic import compute_bubble_regime
from utils import charts

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Industry Bubble Radar", layout="wide")

BASE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(BASE, "assets", "styles.css")) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ---------------- TITLE ----------------
st.title("🧠 Industry Bubble Radar")
st.caption("Institutional early-warning system for bankers & investors")

# ---------------- SIDEBAR ----------------
st.sidebar.header("Controls")

uploaded = st.sidebar.file_uploader("Upload Panel Data", type="csv")
df = pd.read_csv(uploaded) if uploaded else pd.read_csv("data/example_panel_data.csv")

industry = st.sidebar.selectbox("Industry", df["Industry"].unique())
df_i = df[df["Industry"] == industry]

em_th = st.sidebar.slider("Hybrid EM Threshold", 0.5, 3.0, 1.5, 0.1)
peg_th = st.sidebar.slider("PEG Threshold", 1.0, 4.0, 2.5, 0.1)

# ---------------- CORE LOGIC ----------------
regime, score, metrics = compute_bubble_regime(df_i, em_th, peg_th)

st.subheader(f"📌 {industry} Industry Regime")
st.metric("Bubble Risk Score", f"{score}/100")

if "🔴" in regime:
    st.error(regime)
elif "🟠" in regime:
    st.warning(regime)
elif "🟡" in regime:
    st.info(regime)
else:
    st.success(regime)

# ---------------- METRICS ----------------
cols = st.columns(5)
for i,(k,v) in enumerate(metrics.items()):
    cols[i].metric(k, v)

# ---------------- VISUALS ----------------
st.plotly_chart(charts.em_vs_valuation(df_i), use_container_width=True)
st.plotly_chart(charts.risk_quadrant(df_i), use_container_width=True)
st.plotly_chart(charts.industry_heatmap(df), use_container_width=True)
