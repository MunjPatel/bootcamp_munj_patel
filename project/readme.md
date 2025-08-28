# Financial Data Web Scraping  
**Stage:** Problem Framing & Scoping (Stage 01)  

## Problem Statement  
Timely, accurate financial data is essential for investment analysis, risk management, and decision-making. However, much of this information is scattered across multiple websites, APIs, and regulatory portals, often in unstructured formats. Manually collecting and cleaning this data is slow, error-prone, and impractical for high-frequency decision cycles. Automating the collection process through reliable web scraping can streamline data pipelines, reduce operational overhead, and improve the speed at which actionable insights are generated.  

## Stakeholder & User  
- **Stakeholder:** Head of Data Engineering / Chief Investment Officer  
- **Primary Users:** Quantitative analysts, research teams, data scientists  
- **Decision Window:** Data refresh intervals range from real-time (intraday prices) to daily or weekly (macroeconomic reports, filings).  

## Useful Answer & Decision  
- **Type:** Descriptive & Predictive (data ingestion for modeling)  
- **Artifact:** Structured datasets containing cleaned and labeled market, corporate, and macroeconomic data  
- **Decision Trigger:** Automatic pipeline execution at predefined intervals, feeding downstream analytics and models without manual intervention  

## Assumptions & Constraints  
- Target websites permit scraping under their terms of service or provide open APIs  
- Consistent page structure on source sites for parsing stability  
- Storage and processing capacity are sufficient for the anticipated data volume  
- Scrapers run within compliance guidelines, respecting rate limits and jurisdiction-specific data policies  
- Latency tolerance depends on use case (e.g., <1 min for live prices, 1–2 hrs for filings)  

## Known Unknowns / Risks  
- Source website structure changes without notice, breaking scrapers  
- Temporary or permanent data source shutdowns  
- IP blocking or CAPTCHA challenges  
- Data integrity issues if scraping fails mid-run without detection  
- Regulatory changes affecting data usage rights  

## Lifecycle Mapping  
Goal → Stage → Deliverable  
- Identify core financial datasets needed for research → Stage 01 → Scoping document outlining sources, formats, and refresh rates  
- Validate compliance and technical feasibility of scraping → Stage 01 → Risk and compliance checklist  
- Define automation requirements → Stage 01 → Initial scraper architecture plan  

## Repo Plan  
- **Folders:** `/data/`, `/src/`, `/notebooks/`, `/docs/`  
- **Updates:** Codebase updated bi-weekly during development; monitoring scripts updated as source sites change  

# **Market Direction Forecasting with Engineered Financial Signals**

**Stage:** Feature Engineering, Modeling, and Evaluation (Stage 04)

---

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