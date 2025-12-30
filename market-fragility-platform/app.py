import streamlit as st

st.set_page_config(
    page_title="Market Fragility Platform",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown(
    """
    <style>
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    h1, h2, h3 {
        font-weight: 600;
    }
    </style>
    """,
    unsafe_allow_html=True
)
