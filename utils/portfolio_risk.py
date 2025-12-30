def portfolio_stress(portfolio, crash_probs):
    merged = portfolio.merge(
        crash_probs[["Firm", "Crash_Probability"]],
        on="Firm",
        how="left"
    )

    merged["Weighted_Risk"] = (
        merged["Weight"] * merged["Crash_Probability"]
    )

    stress_score = merged["Weighted_Risk"].sum()

    if stress_score > 0.45:
        level = "🔴 Severe Stress"
    elif stress_score > 0.25:
        level = "🟠 Elevated Stress"
    else:
        level = "🟢 Low Stress"

    return stress_score, level, merged
