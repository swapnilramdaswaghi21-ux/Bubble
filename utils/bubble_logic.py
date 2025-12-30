from utils.risk_metrics import em_persistence, concentration_risk, disconnect_index

def compute_bubble_regime(df, em_th, peg_th):
    latest = df[df["Year"] == df["Year"].max()]

    em_share = (latest["Hybrid_EM"] > em_th).mean()
    peg_share = (latest["PEG"] > peg_th).mean()
    avg_f = latest["F_Score"].mean()

    persistence = em_persistence(df, em_th)
    concentration = concentration_risk(df)
    disconnect = disconnect_index(df)

    score = int(100 * (
        0.25 * em_share +
        0.20 * peg_share +
        0.20 * persistence +
        0.20 * concentration +
        0.15 * max(disconnect, 0)
    ))

    if score >= 75:
        regime = "🔴 Fragile Bubble"
    elif score >= 55:
        regime = "🟠 Financial Stretch"
    elif score >= 35:
        regime = "🟡 Narrative Expansion"
    else:
        regime = "🟢 Fundamental Growth"

    return regime, score, {
        "EM Share": round(em_share*100,1),
        "Persistence": round(persistence*100,1),
        "Concentration": round(concentration,2),
        "Disconnect": round(disconnect,2),
        "Avg F-Score": round(avg_f,2)
    }
