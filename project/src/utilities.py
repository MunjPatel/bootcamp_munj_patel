# src/utils.py
import os
import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import BernoulliNB
from sklearn.neural_network import MLPClassifier

sns.set(style="whitegrid")

# ------------------- 
# directory creation 
# ------------------- 
def make_dirs(folder_name: str, parent_directory = '..'):
    directory_path = os.path.join(parent_directory, folder_name)
    if not os.path.exists(directory_path):
        os.makedirs(directory_path, exist_ok=True)
    return directory_path

# -------------------
# DATA INGESTION
# -------------------
def fetch_data(ticker: str, period="max"):
    """Fetch historical OHLCV data from Yahoo Finance."""
    data = yf.Ticker(ticker).history(period=period)
    if {'Dividends', 'Stock Splits'}.issubset(data.columns):
        data = data.drop(columns=['Dividends', 'Stock Splits'])
    return data

# # -------------------
# # CLEAN DATA
# # -------------------
# def clean_data(df: pd.DataFrame):
#     """Handle NaNs, mixed types, and outliers."""
#     df = df.copy()

#     # Convert non-numeric to numeric where possible
#     for col in df.columns:
#         if df[col].dtype == 'object':
#             try:
#                 df[col] = pd.to_numeric(df[col], errors='coerce')
#             except:
#                 pass

#     # Fill NaNs with median
#     df = df.fillna(df.median(numeric_only=True))

#     # Remove extreme outliers using IQR
#     numeric_cols = df.select_dtypes(include=np.number).columns
#     for col in numeric_cols:
#         Q1 = df[col].quantile(0.25)
#         Q3 = df[col].quantile(0.75)
#         IQR = Q3 - Q1
#         lower, upper = Q1 - 1.5 * IQR, Q3 + 1.5 * IQR
#         df[col] = np.clip(df[col], lower, upper)
    
#     return df

# -------------------
# FEATURE ENGINEERING
# -------------------
def engineer_features(df: pd.DataFrame, lookback=14):
    """Generate trading signal features."""
    df = df.copy()
    df['volume_imbalance_signal'] = (df['Close'] - df['Open']) * df['Volume']
    df['volatility_of_pressure'] = df['volume_imbalance_signal'].rolling(window=lookback).std()
    df['intraday_pressure_index'] = (df['High'] - df['Low']) / df['Volume']

    vis_mean = df['volume_imbalance_signal'].rolling(window=lookback).mean()
    vis_std = df['volume_imbalance_signal'].rolling(window=lookback).std(ddof=0)
    df['volume_imbalance_signal_z_score'] = (df['volume_imbalance_signal'] - vis_mean) / vis_std

    df['cumulative_abnormal_pressure'] = df['volume_imbalance_signal_z_score'].rolling(window=lookback).sum()
    df['range_volume_volatility'] = ((df['High'] - df['Low']) / df['Close']) / df['Volume'].rolling(window=lookback).mean()
    df['order_flow_proxy'] = (df['Close'] - (df['High'] - df['Low']) / 2) * df['Volume']
    df['volume_shock_index'] = (df['Volume'] - df['Volume'].rolling(window=lookback).mean()) / df['Volume'].rolling(window=lookback).std()
    df['price_momentum_pressure'] = ((df['Close'] - df['Close'].rolling(window=lookback).mean()) / 
                                     df['Close'].rolling(window=lookback).mean()) * df['Volume']

    df['Close'] = df['Close'].pct_change()
    df['close_direction'] = np.where(df['Close'] > 0, 1, 0)
    return df.dropna()

# -------------------
# MODEL TRAINING
# -------------------
def train_models(X, y):
    """Train multiple baseline models with time-series split."""
    tscv = TimeSeriesSplit(n_splits=10)
    models = {
        "RandomForest": RandomForestClassifier(n_estimators=100, random_state=0),
        "BernoulliNB": BernoulliNB(),
        "MLPClassifier": MLPClassifier(max_iter=500)
    }
    results = {m: [] for m in models}

    for fold_idx, (train_idx, test_idx) in enumerate(tscv.split(X)):
        X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
        y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]

        scaler = StandardScaler()
        X_train = scaler.fit_transform(X_train)
        X_test = scaler.transform(X_test)
        
        if len(X_test) == 0 or len(X_train) == 0:
            print(f"Skipping fold {fold_idx+1} due to empty dataset after cleaning.")
            continue

        for name, model in models.items():
            model.fit(X_train, y_train)
            preds = model.predict(X_test)
            results[name].append(accuracy_score(y_test, preds))
            
        print(f"✅ Completed Fold {fold_idx+1}")
        
    return results

# -------------------
# VISUALIZATIONS
# -------------------
def plot_distribution(df, save_path):
    """Plot numeric feature distributions."""
    numeric_cols = df.select_dtypes(include=np.number).columns
    df[numeric_cols].hist(figsize=(14, 10), bins=30)
    plt.suptitle("Feature Distributions")
    plt.savefig(save_path)
    plt.show()
    plt.close()

def plot_correlation(df, save_path):
    """Correlation heatmap."""
    corr = df.select_dtypes(include=np.number).corr()
    plt.figure(figsize=(12, 8))
    sns.heatmap(corr, annot=True, cmap="coolwarm")
    plt.title("Correlation Heatmap")
    plt.savefig(save_path)
    plt.show()
    plt.close()

# -------------------
# SUMMARY METRICS
# -------------------
def summarize_results(results: dict):
    """Summarize accuracy scores for all models."""
    summary = []
    for model, scores in results.items():
        summary.append({
            'model': model,
            'mean_accuracy': np.mean(scores),
            'std_accuracy': np.std(scores),
            'min_accuracy': np.min(scores),
            'max_accuracy': np.max(scores)
        })
    return pd.DataFrame(summary)
