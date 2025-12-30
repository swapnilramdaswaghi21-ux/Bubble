def build_features(df):
    df = df.copy()
    df["Low_Quality"] = 9 - df["F_Score"]
    df["High_Leverage"] = df["Debt_Equity"]
    df["Weak_Cashflow"] = -df["CFO_Growth"]

    return df[
        ["Hybrid_EM", "PEG", "Low_Quality", "High_Leverage", "Weak_Cashflow"]
    ]
