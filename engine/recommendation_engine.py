def recommend(prob):
    if prob > 0.70:
        return "🔴 Exit / Short"
    elif prob > 0.40:
        return "🟠 Reduce / Hedge"
    else:
        return "🟢 Monitor"
