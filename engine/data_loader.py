import pandas as pd

def load_data(path="data/large_panel_dataset.csv"):
    df = pd.read_csv(path)
    df["Year"] = df["Year"].astype(int)
    return df
