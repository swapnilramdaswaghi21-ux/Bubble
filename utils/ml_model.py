from sklearn.ensemble import GradientBoostingClassifier

def train_crash_model(df, features):
    df = df.copy()
    df["Crash"] = (df["Return"] < -0.30).astype(int)

    X = features
    y = df["Crash"]

    model = GradientBoostingClassifier()
    model.fit(X, y)

    return model
