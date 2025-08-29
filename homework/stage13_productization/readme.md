# Stock Forecasting - Minimal Productization

## Overview

This project demonstrates **basic productization** of a stock forecasting workflow:

* Fetch data from Yahoo Finance

* Build and save a basic model

* Serve predictions via a Flask API

* Provide a clean folder structure for handoff and reuse

## Project Structure

* `data/` - Raw and processed data

* `notebooks/` - Jupyter notebooks for analysis

* `src/` - Reusable Python modules

* `model/` - Saved model (e.g., a pickled model file)

* `reports/` - Charts and PDF summaries

## How to Run

### 1. Clone and Install

First, clone the repository and install the required dependencies:
```bash
git clone <repo-url>
cd stock-forecasting
pip install -r requirements.txt
```

### 2. Run Notebook (Optional - for analysis and model training)
To run the analysis and train/save the model (if applicable), execute the Jupyter notebook:
```bash
jupyter notebook notebooks/stock_analysis.ipynb
```

### 3. Run Flask API
Start the Flask API server:
```bash
python app.py
```

### 4. Test API
Once the Flask API is running, you can test the prediction endpoint using curl:
```bash
curl -X POST [http://127.0.0.1:5000/predict](http://127.0.0.1:5000/predict) \
    -H "Content-Type: application/json" \
    -d '{"last_close": 180.25}'
```

The API should return a JSON response with the predicted close price.

## Working API Screenshot

Below are images demonstrating the working API.

<img src="xxxxx" alt="API Screenshot 1">
<img src="yyyyy" alt="API Screenshot 2">