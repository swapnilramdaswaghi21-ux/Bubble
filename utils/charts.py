import plotly.express as px

def industry_heatmap(df):
    pivot = df.groupby(["Industry","Year"])["Hybrid_EM"].mean().reset_index()
    return px.density_heatmap(
        pivot, x="Year", y="Industry", z="Hybrid_EM",
        color_continuous_scale="Reds",
        title="Industry Bubble Heatmap (Manipulation Intensity)"
    )

def em_vs_valuation(df):
    ts = df.groupby("Year")[["Hybrid_EM","PEG"]].mean().reset_index()
    return px.line(ts, x="Year", y=["Hybrid_EM","PEG"],
                   title="Earnings Manipulation vs Valuation")

def risk_quadrant(df):
    latest = df[df["Year"] == df["Year"].max()]
    return px.scatter(
        latest, x="PEG", y="Hybrid_EM", color="Firm",
        size="F_Score", title="Firm Bubble Risk Quadrant"
    )

