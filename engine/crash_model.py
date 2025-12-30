from sklearn.ensemble import GradientBoostingClassifier

def train_model(df, X):
    y = (df["Return"] < -0.30).astype(int)
    model = GradientBoostingClassifier()
    model.fit(X, y)
    return model

def predict(model, X):
    return model.predict_proba(X)[:,1]
