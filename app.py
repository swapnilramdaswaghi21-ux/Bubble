import streamlit as st
import pandas as pd
import os

from utils.bubble_logic import compute_panel_bubble
from utils import charts

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Industry Bubble Detector", layout="wide")

# ---------------- LOAD CSS SAFELY ----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
css_path = os.path.join(BASE_DIR, "assets", "styles.css")

with open(css_path) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ---------------- TITLE ----------------
st.title("🧠 Industry Bubble Recognition Dashboard")
st.caption("Panel-data based early warning system")

# ---------------- SIDEBAR ----------------
st.sidebar.header("Controls")

uploaded = st.sidebar.file_uploader("Upload Panel Data (CSV)", type="csv")

if uploaded:
    df = pd.read_csv(uploaded)
else:
    df = pd.read_csv("data/example_panel_data.csv")

industry = st.sidebar.selectbox("Select Industry", df["Industry"].unique())
df_ind = df[df["Industry"] == industry]

em_threshold = st.sidebar.slider("Hybrid EM Threshold", 0.5, 3.0, 1.5, 0.1)
peg_threshold = st.sidebar.slider("PEG Threshold", 1.0, 4.0, 2.5, 0.1)
min_share = st.sidebar.slider("Min % Firms with High EM", 0.1, 0.6, 0.3, 0.05)

# ---------------- BUBBLE LOGIC ----------------
verdict, score = compute_panel_bubble(
    df_ind, em_threshold, peg_threshold, min_share
)

st.subheader(f"📌 Verdict for {industry} Industry")

if "🔴" in verdict:
    st.error(f"{verdict} | Risk Score: {score}/100")
elif "🟠" in verdict:
    st.warning(f"{verdict} | Risk Score: {score}/100")
else:
    st.success(f"{verdict} | Risk Score: {score}/100")

# ---------------- CHARTS ----------------
st.plotly_chart(charts.em_vs_valuation(df_ind), use_container_width=True)
st.plotly_chart(charts.firm_distribution(df_ind), use_container_width=True)
st.plotly_chart(charts.em_heatmap(df_ind), use_container_width=True)
st.plotly_chart(charts.quality_trend(df_ind), use_container_width=True)
st.plotly_chart(charts.risk_quadrant(df_ind), use_container_width=True)
st.plotly_chart(
    charts.rolling_probability(df_ind, em_threshold),
    use_container_width=True
)
