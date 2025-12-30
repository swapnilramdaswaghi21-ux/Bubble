import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

def bubble_gauge(score):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        title={"text": "AI Industry Bubble Gauge"},
        gauge={
            "axis": {"range": [0, 100]},
            "bar": {"color": "#ef4444"},
            "steps": [
                {"range": [0, 40], "color": "#064e3b"},
                {"range": [40, 65], "color": "#92400e"},
                {"range": [65, 100], "color": "#7f1d1d"}
            ]
        }
    ))
    return fig


def driver_bar():
    drivers = pd.DataFrame({
        "Driver": ["Real Earnings Manipulation", "Valuation Expansion", "Quality Deterioration"],
        "Contribution": [45, 35, 20]
    })
    return px.bar(drivers, x="Driver", y="Contribution", color="Contribution")
