import pandas as pd

def load_data(file=None):
    if file:
        return pd.read_csv(file)
    return pd.read_csv("data/large_panel_dataset.csv")
