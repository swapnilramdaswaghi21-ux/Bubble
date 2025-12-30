import numpy as np

def em_persistence(df, threshold):
    firm_years = df.sort_values("Year")
    persistent = firm_years.groupby("Firm")["Hybrid_EM"].apply(
        lambda x: (x > threshold).rolling(2).sum().max()
    )
    return (persistent >= 2).mean()

def concentration_risk(df):
    latest = df[df["Year"] == df["Year"].max()]
    top3 = latest.sort_values("Hybrid_EM", ascending=False).head(3)
    return top3["Hybrid_EM"].sum() / latest["Hybrid_EM"].sum()

def disconnect_index(df):
    growth = df.groupby("Year")[["PEG", "Hybrid_EM"]].mean().pct_change()
    return (growth["PEG"] - growth["Hybrid_EM"]).mean()
