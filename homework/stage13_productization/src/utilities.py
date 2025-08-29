import yfinance as yf
import pandas as pd
import numpy as np
import pickle
from sklearn.linear_model import LinearRegression

# -----------------------
# Data Fetching
# -----------------------
def fetch_data(ticker: str, period="1y"):
    """Fetch OHLC data from Yahoo Finance."""
    data = yf.Ticker(ticker).history(period=period)
    data = data[['Close']].reset_index()
    data.rename(columns={'Date': 'date', 'Close': 'close'}, inplace=True)
    return data

# -----------------------
# Feature Engineering
# -----------------------
def engineer_features(df: pd.DataFrame):
    """Create lag features for basic time-series prediction."""
    df = df.copy()
    df['lag1'] = df['close'].shift(1)
    df = df.dropna()
    return df

# -----------------------
# Train and Save Model
# -----------------------
def train_and_save_model(df: pd.DataFrame, model_path="model/model.pkl"):
    X = df[['lag1']].values
    y = df['close'].values
    model = LinearRegression()
    model.fit(X, y)
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)
    return model

# -----------------------
# Load and Predict
# -----------------------
def load_model(model_path="model/model.pkl"):
    with open(model_path, 'rb') as f:
        return pickle.load(f)

def predict_price(model, last_close):
    return float(model.predict(np.array([[last_close]]))[0])
