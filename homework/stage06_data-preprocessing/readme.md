## Data Cleaning Strategy

1. **Missing Values**
   - Numerical columns: imputed using median values.
   - Remaining NaN rows: dropped if imputation was not applicable.
2. **Normalization**
   - All numeric columns normalized using standard scaling (z-score).
3. **Categorical Data**
   - Columns like `city` and `zipcode` left as-is for now (future encoding possible).
4. **Assumptions**
   - Median chosen due to robustness to outliers.
   - At least 15 complete rows required for analysis, ensured during data generation.