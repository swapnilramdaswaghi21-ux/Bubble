from sklearn.ensemble import GradientBoostingClassifier
import numpy as np

def train_model(df, X):
    y = (df["Return"] < -0.30).astype(int)

    # If only one class exists, ML cannot be trained
    if len(np.unique(y)) < 2:
        return None

    model = GradientBoostingClassifier()
    model.fit(X, y)
    return model

def predict(model, X):
    # Fallback scoring when ML is not trainable
    if model is None:
        score = (
            0.4 * X["Hybrid_EM"]
            + 0.3 * X["PEG"]
            + 0.2 * X["High_Leverage"]
            + 0.1 * X["Weak_Cashflow"]
        )
        return score / score.max()

    return model.predict_proba(X)[:, 1]
