<<<<<<< Updated upstream

from __future__ import annotations
import pandas as pd

def train_forecaster(df: pd.DataFrame, horizon_steps: int = 6):
    """Train a LightGBM forecaster for η(t + horizon_steps*10min). Returns (model, importances)."""
    try:
        import lightgbm as lgb
        from sklearn.model_selection import train_test_split
    except Exception as e:
        print("LightGBM/Sklearn missing; skip model training.", e)
        return None, None

    data = df.dropna(subset=["eta"]).copy()
    if len(data) < 400:
        print("Insufficient data for training yet.")
        return None, None

    y = data["eta"].shift(-horizon_steps)
    X = data.drop(columns=["eta"]).select_dtypes(include=['float','int']).iloc[:-horizon_steps]
    y = y.iloc[:-horizon_steps]
    X = X.loc[y.index]

    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.25, shuffle=False)
    model = lgb.LGBMRegressor(n_estimators=400, learning_rate=0.03, subsample=0.9, colsample_bytree=0.9)
    model.fit(Xtr, ytr, eval_set=[(Xte, yte)], eval_metric="l2", verbose=False)
    importances = pd.Series(model.feature_importances_, index=X.columns).sort_values(ascending=False)
    return model, importances
=======

from __future__ import annotations
import pandas as pd

def train_forecaster(df: pd.DataFrame, horizon_steps: int = 6):
    """Train a LightGBM forecaster for η(t + horizon_steps*10min). Returns (model, importances)."""
    try:
        import lightgbm as lgb
        from sklearn.model_selection import train_test_split
    except Exception as e:
        print("LightGBM/Sklearn missing; skip model training.", e)
        return None, None

    data = df.dropna(subset=["eta"]).copy()
    if len(data) < 400:
        print("Insufficient data for training yet.")
        return None, None

    y = data["eta"].shift(-horizon_steps)
    X = data.drop(columns=["eta"]).select_dtypes(include=['float','int']).iloc[:-horizon_steps]
    y = y.iloc[:-horizon_steps]
    X = X.loc[y.index]

    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.25, shuffle=False)
    model = lgb.LGBMRegressor(n_estimators=400, learning_rate=0.03, subsample=0.9, colsample_bytree=0.9)
    model.fit(Xtr, ytr, eval_set=[(Xte, yte)], eval_metric="l2", verbose=False)
    importances = pd.Series(model.feature_importances_, index=X.columns).sort_values(ascending=False)
    return model, importances
>>>>>>> Stashed changes
