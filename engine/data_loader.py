import pandas as pd

def load_data(file=None):
    if file is not None:
        return pd.read_csv(file)
    return pd.read_csv("data/large_panel_dataset.csv")

