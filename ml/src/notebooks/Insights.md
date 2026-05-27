# Exploratory Data Analysis (EDA) Insights

## 1. Correlation Heatmap Analysis

### Key Patterns Observed

- `totalIncome`, `totalOutcome`, and `totalNumberTransaction` show very strong positive correlations.
- `numberIncomeTransaction` and `numberOutcomeTransaction` are also strongly correlated with total transaction activity.
- `totalBalance` has weak correlation with most other variables.

### Business Insights

- Transaction activity is the primary driver of ATM cash movement.
- ATMs with higher transaction counts naturally require more frequent cash replenishment.
- Current balance alone is not enough to accurately forecast future cash demand.

### Forecasting Insights

The following features are highly useful for ATM cash forecasting:

- `totalOutcome`
- `numberOutcomeTransaction`
- `totalNumberTransaction`
- `totalBalance`

### Important Observation

Strong multicollinearity exists between several transaction-related features. Tree-based machine learning models such as Random Forest and XGBoost may perform better than simple linear models for this dataset.

---

## 2. Transactions by Day of Week

### Patterns Observed

- Transaction counts are relatively similar across all weekdays.
- No major difference exists between weekdays and weekends.

### Business Insights

- ATM usage appears stable throughout the week.
- This suggests consistent customer behavior and predictable ATM demand.

### Forecasting Insights

- Day-of-week may have only a small influence on forecasting accuracy.
- However, it should still be included as a feature because small cyclical trends may exist.

### Additional Improvement

This graph only shows record counts. More useful analysis could include:

- Average withdrawal amount per day
- Total withdrawals per day
- Median transactions per day

---

## 3. Boxplot Analysis

### Patterns Observed

- Transaction distributions are almost identical across all days.
- Median transaction values remain consistent.
- Data spread is also very similar for each day.

### Business Insights

- ATM demand is operationally stable.
- No single day experiences unusually high transaction spikes.

### Forecasting Insights

- Stable distributions make forecasting easier and improve model learning.
- Lower volatility helps reduce sudden cash shortage risks.

### Anomalies

- Very few outliers are visible.
- Real-world ATM systems usually contain spikes during:
  - Salary dates
  - Festivals
  - Holidays
  - Month-end periods

This dataset may therefore be relatively clean or partially normalized.

---

## 4. Histogram Distribution Analysis

## Total Balance

### Observations

- Most ATMs maintain balances near the upper balance range.

### Business Insights

- Banks likely maintain safety cash thresholds inside ATMs.

### Forecasting Insights

- Useful for low-cash alert systems and refill scheduling.

---

## Number of Outcome Transactions

### Observations

- A bimodal distribution is visible.

### Business Insights

- Multiple ATM behavior groups may exist:
  - Low-demand ATMs
  - High-demand ATMs

### Forecasting Insights

- ATM segmentation can significantly improve forecasting accuracy.

---

## Total Income and Total Outcome

### Observations

- Both distributions are skewed.
- Most ATMs operate within predictable transaction ranges.

### Business Insights

- ATM cash movement is concentrated within specific operating ranges.

### Forecasting Insights

- Feature scaling or log transformation may improve regression model performance.

---

## Total Number of Transactions

### Observations

- Another bimodal pattern is visible.

### Business Insights

- All ATMs do not behave similarly.
- Different ATM categories may exist based on customer activity.

### Forecasting Insights

- Cluster-based forecasting may outperform a single global model.

---

## 5. ATM Comparison Bar Charts

### Patterns Observed

- Top-performing ATMs show very similar transaction totals.
- No ATM appears extremely dominant.

### Business Insights

- ATM demand is relatively balanced across the network.
- Cash refill operations can potentially be standardized.

### Forecasting Insights

- Balanced ATM behavior simplifies demand forecasting.
- Similarity between ATMs may also indicate capped or normalized values in the dataset.

---

## Overall Forecasting Insights

## Most Important Predictive Features

The strongest features for ATM cash forecasting are likely:

1. `totalOutcome`
2. `numberOutcomeTransaction`
3. `totalNumberTransaction`
4. `totalBalance`
5. Time-based features (`day`, `hour`, `month`)

---

# Final Conclusion

The analysis suggests that:

- ATM demand is relatively stable.
- Transaction-related variables dominate forecasting performance.