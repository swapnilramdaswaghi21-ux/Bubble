import plotly.express as px
import plotly.graph_objects as go

def em_vs_valuation(df):
    ts = df.groupby("Year")[["Hybrid_EM", "PEG"]].mean().reset_index()
    return px.line(ts, x="Year", y=["Hybrid_EM", "PEG"],
                   title="Earnings Manipulation vs Valuation")

def firm_distribution(df):
    latest = df[df["Year"] == df["Year"].max()]
    return px.bar(latest, x="Firm", y="Hybrid_EM",
                  title="Firm-Level Manipulation Risk")

def em_heatmap(df):
    pivot = df.pivot(index="Firm", columns="Year", values="Hybrid_EM")
    return px.imshow(pivot, color_continuous_scale="Reds",
                     title="Earnings Manipulation Heatmap")

def quality_trend(df):
    q = df.groupby("Year")["F_Score"].mean().reset_index()
    return px.line(q, x="Year", y="F_Score",
                   title="Financial Quality (F-Score) Trend")

def risk_quadrant(df):
    latest = df[df["Year"] == df["Year"].max()]
    return px.scatter(
        latest,
        x="PEG",
        y="Hybrid_EM",
        size="F_Score",
        color="Firm",
        title="Bubble Risk Quadrant",
        hover_name="Firm"
    )

def rolling_probability(df, em_threshold):
    roll = df.groupby("Year").apply(
        lambda x: (x["Hybrid_EM"] > em_threshold).mean()
    ).reset_index(name="Probability")
    return px.line(roll, x="Year", y="Probability",
                   title="Rolling Bubble Probability")
