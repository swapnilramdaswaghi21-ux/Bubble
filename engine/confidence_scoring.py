def confidence_score(df):
    years = df["Year"].nunique()
    if years >= 7:
        return "High"
    elif years >= 4:
        return "Medium"
    else:
        return "Low"
