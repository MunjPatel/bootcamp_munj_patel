Orchestration Plan: Stock Forecasting Pipeline
Overview

This document outlines the orchestration plan for the stock forecasting project, detailing the key tasks, their dependencies, input/output artifacts, logging, checkpointing strategies, and automation decisions. The goal is to build a robust and maintainable machine learning pipeline.
Project Tasks and Dependencies (DAG)

The stock forecasting pipeline can be broken down into five primary tasks with sequential dependencies:

    Ingest Raw Data: Downloads historical OHLCV data for a specified ticker.

    Feature Engineering: Transforms raw data into a set of engineered features.

    Data Preparation (PCA & Scaling): Applies StandardScaler and PCA to the features.

    Model Training: Trains the RandomForestClassifier on the prepared features and target.

    Model Saving: Serializes and saves the trained model and transformers.

graph TD
    A[Ingest Raw Data] --> B[Feature Engineering]
    B --> C[Data Preparation (PCA & Scaling)]
    C --> D[Model Training]
    D --> E[Model Saving]

Task Details

Task
	

Input(s)
	

Output(s)
	

Idempotency
	

Logging & Checkpoint Strategy
	

Failure Points & Retry

1. Ingest Raw Data
	

Ticker Symbol, Period
	

data/raw/{ticker}_ohlcv.csv
	

Yes
	

Log start/end, API errors to logs/pipeline.log. Checkpoint ohlcv.csv.
	

Network errors, API rate limits. Retry: 3x with exponential backoff.

2. Feature Engineering
	

data/raw/{ticker}_ohlcv.csv
	

data/processed/features_df.csv
	

Yes
	

Log feature calculation progress/errors to logs/pipeline.log. Checkpoint features_df.csv.
	

NaN/Inf introduction. Fail fast, alert data owner.

3. Data Preparation (PCA & Scaling)
	

data/processed/features_df.csv
	

data/processed/scaled_features.pkl, model/scaler.pkl, model/pca.pkl
	

Yes
	

Log scaling/PCA parameters to logs/pipeline.log. Checkpoint scaled_features.pkl.
	

Invalid data types/schema drift. Fail fast, alert ML Engineer.

4. Model Training
	

data/processed/scaled_features.pkl, Target (close_direction)
	

model/trained_model.pkl (temporary)
	

Pseudo-Yes*
	

Log training metrics (accuracy, loss), warnings (e.g., convergence), start/end to logs/pipeline.log.
	

Poor performance (accuracy < 0.52). Log warning, proceed to saving but flag for review. No automated retry.

5. Model Saving
	

Trained Model, Scaler, PCA objects
	

model/model.pkl, model/scaler.pkl, model/pca.pkl
	

Yes
	

Log model saving path and timestamp to logs/pipeline.log.
	

Disk I/O errors. Retry: 1x, then alert system admin.

*Idempotency for Model Training is "Pseudo-Yes" because while the process is deterministic with fixed random seeds, different runs might yield slightly different weights/trees. However, it always produces a trained model for the given data and parameters.
Automation Decisions

    Automate Immediately: Tasks 1-5 (Ingest, Feature Engineering, Data Preparation, Model Training, Model Saving) will be automated to run nightly via a scheduled job. This ensures the model is regularly updated with fresh data.

    Keep Manual:

        Model Evaluation & Approval: Final review of model performance, business impact, and A/B test results before production deployment requires human judgment.

        Deployment to Production (Flask API): Rolling out new model versions to the serving API will be a manual or semi-automated process with explicit approval, as it directly impacts users and critical systems.

        Advanced Debugging & Root Cause Analysis: Complex failures or unexpected model behavior will trigger alerts requiring manual investigation by the ML Engineer.

This phased approach balances the need for timely model updates with controlled deployment, leveraging automation where feasible while retaining human oversight for critical decisions.