import pandas as pd

def backtest_crashes(df, model, feature_func):
    results = []

    for year in sorted(df["Year"].unique())[:-1]:
        train = df[df["Year"] < year]
        test = df[df["Year"] == year]

        # Require minimum history
        if len(train) < 10 or len(test) == 0:
            continue

        X_train = feature_func(train)
        y_train = (train["Return"] < -0.30).astype(int)

        model.fit(X_train, y_train)

        X_test = feature_func(test)
        probs = model.predict_proba(X_test)[:, 1]

        test = test.copy()
        test["Predicted_Prob"] = probs
        results.append(test)

    # 🚨 CRITICAL FIX — prevents crash
    if len(results) == 0:
        return pd.DataFrame()

    return pd.concat(results, ignore_index=True)
