def compute_bubble_score(df):
    high_em_pct = round((df["Hybrid_EM"] > 1.5).mean() * 100, 0)
    avg_peg = round(df["PEG"].mean(), 2)
    avg_f = df["F_Score"].mean()

    score = int(
        0.4 * (high_em_pct / 100) * 100 +
        0.3 * (avg_peg / 3) * 100 +
        0.3 * ((9 - avg_f) / 9) * 100
    )

    verdict = score >= 65

    metrics = {
        "high_em_pct": high_em_pct,
        "avg_peg": avg_peg
    }

    return score, metrics, verdict
