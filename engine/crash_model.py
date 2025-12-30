from sklearn.ensemble import GradientBoostingClassifier

def train_model(df, X):
    df = df.copy()
    df["Crash"] = (df["Return"] < -0.30).astype(int)

    model = GradientBoostingClassifier()
    model.fit(X, df["Crash"])
    return model

def predict_probabilities(model, X):
    return model.predict_proba(X)[:, 1]
