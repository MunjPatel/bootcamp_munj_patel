Reflection: Deployment & Monitoring

This stock forecasting project, using features derived from OHLCV data and a binary classification target (close_direction), presents several deployment risks. My current Random Forest Classifier, if deployed, could face data drift (market conditions change), feature drift/schema drift (upstream data source or feature calculation changes), and model staleness (predictive power degrading over time).

To mitigate these, comprehensive monitoring is critical across four layers:

    Data Layer:

        Metric: Daily Data Freshness (time since last yf.Ticker().history() fetch). Threshold: > 30 minutes.

        Metric: Null Rate for volume_imbalance_signal. Threshold: > 0.1% daily.

        Metric: Population Stability Index (PSI) for order_flow_proxy. Threshold: PSI > 0.1 over a 7-day window.

    Model Layer:

        Metric: Rolling 7-day Accuracy. Threshold: < 0.52 (slightly above random chance).

        Metric: Prediction Bias (mean of positive class probabilities). Threshold: Outside 0.45 - 0.55 range for 7-day window.

    System Layer:

        Metric: Flask /predict endpoint p95 latency. Threshold: > 500 ms.

        Metric: API Error Rate (HTTP 5xx responses). Threshold: > 1% in a 5-minute window.

    Business Layer:

        Metric: Daily "Actionable Signal Rate" (e.g., days with prediction confidence > 0.6). Threshold: < 10% or > 80%.

Ownership and Maintenance:
Ongoing maintenance, dashboard updates, and alert responses would be owned by an ML Engineer / Data Scientist. DevOps/SRE would handle system-level alerts. Alert recipients would be specific teams/individuals based on the layer. The initial runbook step for a data alert would be to investigate data pipeline logs; for a model alert, it would involve reviewing recent feature distributions.

Retraining:
The model would be retrained weekly after market close on Friday. Retraining would also be triggered if the PSI for order_flow_proxy exceeds 0.2 over a 30-day window, or if the rolling 30-day accuracy drops below 0.55. Rollback approvals for model issues reside with the ML Engineer, while system rollbacks involve DevOps/SRE. All incidents and issues are logged in a central system (e.g., JIRA) for tracking and post-mortem analysis.