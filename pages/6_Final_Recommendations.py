import streamlit as st
from engine.confidence_scoring import confidence_score
from engine.data_loader import load_data

df = load_data()

st.header("✅ Final Risk Assessment & Recommendations")

confidence = confidence_score(df)

st.markdown("""
### 🔍 Key Findings
• Bubble-like characteristics detected in select industries  
• Crash vulnerability is concentrated in a small set of firms  

### 🚨 First Firms Likely to Crack
• High earnings manipulation  
• Weak cash flows  
• Elevated leverage  

### 📌 Recommendation
**Reduce exposure, hedge downside risk, avoid new long positions in high-risk firms.**
""")

st.metric("Confidence Level", confidence)
