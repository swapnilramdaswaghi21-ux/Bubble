def compute_panel_bubble(df, em_threshold, peg_threshold, min_share):
    latest_year = df["Year"].max()
    df_latest = df[df["Year"] == latest_year]

    high_em_share = (df_latest["Hybrid_EM"] > em_threshold).mean()
    high_peg_share = (df_latest["PEG"] > peg_threshold).mean()
    avg_f = df_latest["F_Score"].mean()

    bubble_score = int(
        100 * (
            0.4 * high_em_share +
            0.3 * high_peg_share +
            0.3 * ((9 - avg_f) / 9)
        )
    )

    if bubble_score >= 70 and high_em_share >= min_share:
        verdict = "🔴 Bubble Detected"
    elif bubble_score >= 45:
        verdict = "🟠 Bubble Building"
    else:
        verdict = "🟢 No Bubble"

    return verdict, bubble_score

