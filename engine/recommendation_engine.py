def recommend(p):
    if p > 0.70:
        return "🔴 Exit / Short"
    elif p > 0.40:
        return "🟠 Reduce / Hedge"
    else:
        return "🟢 Monitor"
