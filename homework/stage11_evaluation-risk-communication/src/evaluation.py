import numpy as np
from sklearn.metrics import mean_squared_error

def bootstrap_ci(X_test, y_test, model, n_bootstrap=500, metric="rmse"):
    np.random.seed(42)
    n = len(y_test)
    stats = []

    for _ in range(n_bootstrap):
        indices = np.random.choice(n, n, replace=True)
        X_bs = X_test[indices]
        y_bs = y_test[indices]
        y_pred = model.predict(X_bs)

        if metric == "rmse":
            stat = mean_squared_error(y_bs, y_pred, squared=False)
        else:
            raise ValueError("Unsupported metric")

        stats.append(stat)

    return stats
