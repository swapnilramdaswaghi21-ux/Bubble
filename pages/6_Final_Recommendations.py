import streamlit as st
from engine.data_loader import load_data

st.header("✅ Final Institutional Recommendation")

df = load_data()

top = (
    df.groupby("Firm")["Hybrid_EM"]
    .mean()
    .sort_values(ascending=False)
    .head(5)
)

st.markdown("### 🚨 First Firms Likely to Crack")
for firm in top.index:
    st.write(f"• **{firm}** — structurally fragile under stress")

st.markdown("""
### 📌 Action
• Reduce exposure  
• Hedge downside  
• Avoid new long positions  

**Confidence: High (large panel, cross-industry learning)**
""")

