import pandas as pd

def backtest_crashes(df, model, feature_func):
    results = []

    for year in sorted(df["Year"].unique())[:-1]:
        train = df[df["Year"] < year]
        test = df[df["Year"] == year]

        if len(train) < 10:
            continue

        X_train = feature_func(train)
        X_test = feature_func(test)

        model.fit(X_train, (train["Return"] < -0.30).astype(int))
        probs = model.predict_proba(X_test)[:,1]

        test = test.copy()
        test["Predicted_Prob"] = probs
        results.append(test)

    return pd.concat(results)
