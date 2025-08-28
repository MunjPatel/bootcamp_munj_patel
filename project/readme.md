# **Market Direction Forecasting with Engineered Financial Signals**

## **Problem Statement**

Predicting short-term market direction is critical for trading strategies, portfolio hedging, and risk management. Traditional price-only models often underperform because they fail to capture complex relationships in market microstructure data, such as volume pressure, order flow, and abnormal momentum.  

This project builds a pipeline to:
- **Ingest historical data** for the S&P 500 index (`^GSPC`) via the `yfinance` API.  
- **Engineer advanced market signals** (volume imbalance, order flow proxies, cumulative abnormal pressure, etc.).  
- **Evaluate predictive performance** using machine learning models to classify daily close direction (up/down).

---

## **Stakeholders & Users**
- **Stakeholders:** Quantitative trading desks, portfolio managers, risk teams  
- **Primary Users:** Quantitative analysts, data scientists, algorithmic traders  
- **Decision Windows:** Daily or intraday signals to adjust positions and risk exposures  

---

## **Approach & Workflow**
1. **Data Ingestion:** Download full-history OHLCV data for `^GSPC`.  
2. **Feature Engineering:** Create derived signals capturing volume-pressure dynamics, abnormal flows, and momentum-pressure relationships.  
3. **Dimensionality Reduction:** Apply PCA to handle feature correlation and isolate key explanatory components.  
4. **Modeling:** Train and validate three baseline models with time-series splits:
   - **RandomForestClassifier**
   - **BernoulliNB**
   - **MLPClassifier**
5. **Evaluation:** Use accuracy, cross-fold stability, and feature importance to compare model effectiveness.  

---

## **Key Findings**
| Model | Average Accuracy | Std. Dev. | Notes |
|--------|----------------|-----------|-------|
| **RandomForestClassifier** | ~0.876 | ±0.029 | Stable performance; interpretable feature importance |
| **BernoulliNB** | ~0.877 | ±0.026 | Surprisingly competitive despite simplicity |
| **MLPClassifier** | ~0.836 | ±0.059 | Potential to improve with hyperparameter tuning |

**Top Predictive Signals:**  
1. **Volume Imbalance Z-Score (~74% importance)**  
2. **Cumulative Abnormal Pressure (~11%)**  
3. **Volatility of Pressure (~7%)**  
4. **Order Flow Proxy (~7%)**

---

## **Assumptions & Risks**
- Market microstructure relationships are **stationary** over the training period.  
- Data from Yahoo Finance is accurate and complete.  
- Outliers are genuine market events, not data errors.  
- **Risks:**
  - PCA and engineered signals might overfit historical patterns.
  - Market regime changes may reduce predictive power.
  - Volume-based features may degrade in low-liquidity environments.

## **Repo Structure**
- **Folders:** `/data/`, `/src/`, `/notebooks/`, `/docs/`, `/figures/`

## **Next Steps**
- Hyperparameter tuning for `MLPClassifier` to improve convergence and stability.  
- Explore advanced ensemble methods (e.g., XGBoost, Gradient Boosting).  
- Add lagged feature sets to capture delayed signal effects.  
- Conduct out-of-sample and walk-forward validation for robustness.  