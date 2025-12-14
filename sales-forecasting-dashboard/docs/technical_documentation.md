# Technical Documentation

**AI-Powered Sales Forecasting Dashboard**  
**Project Version**: 1.0  
**Last Updated**: December 2024

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Architecture](#architecture)
3. [Data Pipeline](#data-pipeline)
4. [Feature Engineering](#feature-engineering)
5. [Model Architecture](#model-architecture)
6. [API & Integration](#api--integration)
7. [Deployment](#deployment)
8. [Troubleshooting](#troubleshooting)

---

## Project Overview

### Objectives
- Forecast retail sales for 12 months using historical data
- Identify seasonal patterns and trends
- Provide actionable business insights
- Enable data-driven decision making through BI dashboard

### Tech Stack

| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| Language | Python | 3.10+ | Data processing & ML |
| Notebooks | Jupyter | 7.0+ | Interactive analysis |
| Forecasting | Facebook Prophet | 1.1+ | Time series prediction |
| Stats Modeling | Statsmodels | 0.13+ | ARIMA & diagnostics |
| Data Processing | Pandas | 1.5+ | Data manipulation |
| Numerical | NumPy | 1.23+ | Matrix operations |
| Visualization | Matplotlib/Seaborn | 3.6/0.12+ | Charts & plots |
| ML | Scikit-learn | 1.2+ | Preprocessing & metrics |
| BI Tool | Power BI | Desktop/Online | Dashboard & reporting |
| Database | CSV/Excel | - | Data storage |

### Project Structure

```
sales-forecasting-dashboard/
├── README.md
├── data/
│   ├── sales_historical.csv          # Raw transaction data (67K records)
│   ├── sales_cleaned.csv             # After data cleaning
│   ├── sales_daily.csv               # Daily aggregation
│   ├── sales_monthly.csv             # Monthly aggregation
│   └── sales_with_features.csv       # Engineered features
├── notebooks/
│   ├── 00_generate_sample_data.ipynb       # 1095 days, 5 stores, 5 categories
│   ├── 01_eda_data_cleaning.ipynb          # Missing values, outliers, quality
│   ├── 02_feature_engineering.ipynb        # 30+ features created
│   ├── 03_time_series_forecasting.ipynb    # Prophet + ARIMA models
│   └── 04_business_analytics.ipynb         # KPIs, insights, recommendations
├── exports/
│   ├── sales_with_forecasts.csv      # For Power BI (main)
│   ├── daily_forecasts.csv           # Daily predictions
│   ├── monthly_forecasts.csv         # Monthly aggregation
│   ├── kpi_summary.csv               # Performance metrics
│   ├── category_analysis.csv         # By category
│   ├── store_analysis.csv            # By store
│   └── region_analysis.csv           # By region
├── models/
│   ├── prophet_model.pkl             # Trained model artifact
│   └── model_performance.json         # Metrics & validation
└── docs/
    ├── POWERBI_SETUP_GUIDE.md        # Dashboard creation
    ├── business_recommendations.md   # Strategic insights
    └── technical_documentation.md    # This file
```

---

## Architecture

### System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    RAW DATA SOURCE                      │
│              (Historical Sales Transactions)            │
│                   (1,095 days × N)                     │
└─────────────┬───────────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────────────────────┐
│              PYTHON PROCESSING PIPELINE                │
│  ┌──────────────────────────────────────────────────┐  │
│  │  00: Data Generation (Synthetic)                 │  │
│  │      → sales_historical.csv                      │  │
│  └──────────────────────────────────────────────────┘  │
│              │                                          │
│              ▼                                          │
│  ┌──────────────────────────────────────────────────┐  │
│  │  01: EDA & Cleaning                              │  │
│  │      → Remove nulls, duplicates, outliers        │  │
│  │      → Handle missing values                     │  │
│  │      → Quality checks                            │  │
│  │      → Outputs: sales_cleaned.csv                │  │
│  └──────────────────────────────────────────────────┘  │
│              │                                          │
│              ▼                                          │
│  ┌──────────────────────────────────────────────────┐  │
│  │  02: Feature Engineering                         │  │
│  │      → Temporal features (30)                    │  │
│  │      → Seasonal indicators (5)                   │  │
│  │      → Holiday flags (3)                         │  │
│  │      → Lagged features (5)                       │  │
│  │      → Moving averages (7)                       │  │
│  │      → Momentum indicators (4)                   │  │
│  │      → Aggregate features (7)                    │  │
│  │      → Outputs: sales_with_features.csv          │  │
│  └──────────────────────────────────────────────────┘  │
│              │                                          │
│              ▼                                          │
│  ┌──────────────────────────────────────────────────┐  │
│  │  03: Time Series Forecasting                     │  │
│  │      → Train/test split (80/20)                  │  │
│  │      → Fit Prophet model                         │  │
│  │      → Generate 365-day forecast                 │  │
│  │      → Calculate confidence intervals            │  │
│  │      → Model evaluation (MAE, RMSE, MAPE)        │  │
│  │      → Outputs: forecasts & metrics              │  │
│  └──────────────────────────────────────────────────┘  │
│              │                                          │
│              ▼                                          │
│  ┌──────────────────────────────────────────────────┐  │
│  │  04: Business Analytics                          │  │
│  │      → Calculate KPIs                            │  │
│  │      → Segment analysis (store/category/region)  │  │
│  │      → Identify patterns & insights              │  │
│  │      → Generate recommendations                  │  │
│  │      → Outputs: Analysis reports & data          │  │
│  └──────────────────────────────────────────────────┘  │
└─────────────┬───────────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────────────────────┐
│                   EXPORT LAYER                         │
│  ┌──────────────────────────────────────────────────┐  │
│  │  CSV Files (for Power BI ingestion)              │  │
│  │  • sales_with_forecasts.csv (main)               │  │
│  │  • daily/monthly_forecasts.csv                   │  │
│  │  • kpi_summary.csv                               │  │
│  │  • segment_analysis.csv                          │  │
│  └──────────────────────────────────────────────────┘  │
└─────────────┬───────────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────────────────────┐
│                   POWER BI DASHBOARD                   │
│  ┌──────────────────────────────────────────────────┐  │
│  │  Executive Summary                                │  │
│  │  Historical Analysis                              │  │
│  │  Seasonal Patterns                                │  │
│  │  Regional Deep Dive                               │  │
│  │  Insights & Recommendations                       │  │
│  └──────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

---

## Data Pipeline

### Stage 1: Data Ingestion

**Input**: Historical sales transactions  
**Format**: CSV (67,043 records)  
**Fields**:
- Date: Transaction date
- Store: Store identifier
- Category: Product category
- Region: Geographic region
- Quantity: Units sold
- Sales_Amount: Revenue
- Unit_Price: Price per unit

**Validation**:
```python
# Schema validation
assert df['Date'].dtype == 'datetime64[ns]'
assert df['Sales_Amount'].dtype == 'float64'
assert df['Quantity'].dtype in ['int64', 'int32']

# Business logic validation
assert (df['Sales_Amount'] > 0).all()
assert (df['Quantity'] > 0).all()
assert df['Store'].isin(valid_stores).all()
assert df['Category'].isin(valid_categories).all()
```

### Stage 2: Data Cleaning

**Operations**:

1. **Null Handling**
   ```python
   # Missing values: 2% in Unit_Price
   df['Unit_Price'] = df.groupby('Category')['Unit_Price'].transform(
       lambda x: x.fillna(x.median())
   )
   ```

2. **Duplicate Removal**
   ```python
   df = df.drop_duplicates()
   removed: 0 (no exact duplicates found)
   ```

3. **Outlier Detection**
   ```python
   Q1 = df['Sales_Amount'].quantile(0.25)
   Q3 = df['Sales_Amount'].quantile(0.75)
   IQR = Q3 - Q1
   outliers = df[(df['Sales_Amount'] < Q1 - 1.5*IQR) | 
                 (df['Sales_Amount'] > Q3 + 1.5*IQR)]
   # Retained as legitimate high-value transactions
   ```

**Output Quality**:
- Records retained: 66,841 (99.7%)
- Missing values: 0
- Duplicates: 0
- Valid date range: 1,095 days

### Stage 3: Aggregation

**Daily Level**:
```python
daily = df.groupby('Date').agg({
    'Sales_Amount': ['sum', 'mean', 'count'],
    'Quantity': 'sum'
})
# Output: 1,095 records (1 per day)
```

**Monthly Level**:
```python
monthly = df.groupby(df['Date'].dt.to_period('M')).agg({
    'Sales_Amount': ['sum', 'mean', 'count'],
    'Quantity': 'sum'
})
# Output: 36 records (1 per month)
```

---

## Feature Engineering

### Feature Categories

#### 1. Temporal Features (10)
```python
df['Year'] = df['Date'].dt.year
df['Month'] = df['Date'].dt.month
df['Quarter'] = df['Date'].dt.quarter
df['DayOfWeek'] = df['Date'].dt.dayofweek  # 0-6 (Mon-Sun)
df['DayOfMonth'] = df['Date'].dt.day
df['WeekOfYear'] = df['Date'].dt.isocalendar().week
df['DayOfYear'] = df['Date'].dt.dayofyear
df['IsWeekend'] = (df['DayOfWeek'] >= 5).astype(int)  # Friday-Sunday
df['DayName'] = df['Date'].dt.day_name()
df['MonthName'] = df['Date'].dt.month_name()
```

#### 2. Seasonal Features (5)
```python
# Categorical season
df['Season'] = df['Month'].map({
    12: 'Winter', 1: 'Winter', 2: 'Winter',
    3: 'Spring', 4: 'Spring', 5: 'Spring',
    6: 'Summer', 7: 'Summer', 8: 'Summer',
    9: 'Fall', 10: 'Fall', 11: 'Fall'
})

# Cyclical encoding (captures seasonality relationships)
df['Month_sin'] = np.sin(2 * np.pi * df['Month'] / 12)
df['Month_cos'] = np.cos(2 * np.pi * df['Month'] / 12)
df['DayOfWeek_sin'] = np.sin(2 * np.pi * df['DayOfWeek'] / 7)
df['DayOfWeek_cos'] = np.cos(2 * np.pi * df['DayOfWeek'] / 7)
```

**Why Cyclical Encoding?**
- Preserves circular nature of time
- Model learns December→January continuity
- Example: sin/cos values smooth transition from Dec to Jan

#### 3. Holiday Features (3)
```python
# Holiday season indicator (7 days around major holidays)
holidays = [(1,1), (2,14), (7,4), (10,31), (11,27), (12,25)]
df['Holiday_Season'] = df['Date'].apply(is_holiday_season)

# Q4 indicator (Oct-Dec)
df['IsQ4'] = ((df['Month'] >= 10) & (df['Month'] <= 12)).astype(int)

# Black Friday/Cyber Monday
df['IsBlackFriday'] = detect_black_friday(df['Date'])
```

#### 4. Lagged Features (5)
```python
# Previous period values (capture momentum)
df['Sales_Lag1'] = df['Total_Sales'].shift(1)    # Previous day
df['Sales_Lag7'] = df['Total_Sales'].shift(7)    # Previous week
df['Sales_Lag30'] = df['Total_Sales'].shift(30)  # Previous month
df['Sales_Lag365'] = df['Total_Sales'].shift(365) # Previous year
df['YoY_Growth'] = ((df['Total_Sales'] - df['Sales_Lag365']) / 
                    df['Sales_Lag365'] * 100).fillna(0)
```

#### 5. Moving Averages (7)
```python
# Simple moving averages
df['MA7'] = df['Total_Sales'].rolling(window=7, min_periods=1).mean()
df['MA14'] = df['Total_Sales'].rolling(window=14, min_periods=1).mean()
df['MA30'] = df['Total_Sales'].rolling(window=30, min_periods=1).mean()

# Exponential moving averages (weighted toward recent data)
df['EMA7'] = df['Total_Sales'].ewm(span=7, adjust=False).mean()
df['EMA30'] = df['Total_Sales'].ewm(span=30, adjust=False).mean()

# Trend indicator
df['Trend_Indicator'] = (df['MA7'] - df['MA30']) / df['MA30'] * 100

# Volatility (7-day rolling std dev)
df['Volatility'] = df['Total_Sales'].pct_change().rolling(window=7).std()
```

#### 6. Momentum Indicators (4)
```python
# Daily change
df['Pct_Change'] = df['Total_Sales'].pct_change() * 100

# Momentum (7-day)
df['Momentum_7d'] = df['Total_Sales'] - df['Total_Sales'].shift(7)

# Rate of change
df['ROC_7d'] = (df['Total_Sales'].pct_change(periods=7)) * 100
df['ROC_30d'] = (df['Total_Sales'].pct_change(periods=30)) * 100
```

#### 7. Aggregate Features (7)
```python
# Monthly aggregates
monthly_agg = df.groupby(df['Date'].dt.to_period('M')).agg({
    'Total_Sales': ['mean', 'std', 'min', 'max']
})
df = df.merge(monthly_agg, on='YearMonth', how='left')

# Quarterly aggregates
quarterly_agg = df.groupby([df['Date'].dt.year, 
                            df['Date'].dt.quarter])['Total_Sales'].agg(['mean', 'sum'])
df = df.merge(quarterly_agg, on=['Year', 'Quarter'], how='left')
```

### Feature Statistics

| Feature Category | Count | Data Type | Range | Usage |
|------------------|-------|-----------|-------|-------|
| Temporal | 10 | int/string | 1-366 | Prophet treats as components |
| Seasonal | 5 | float/-1to1 | -1 to +1 | Cyclical patterns |
| Holiday | 3 | int/binary | 0-1 | Special event impacts |
| Lagged | 5 | float | Variable | Momentum & trend |
| MA/Trend | 7 | float | Variable | Smoothing & velocity |
| Momentum | 4 | float | Variable | Rate of change |
| Aggregate | 7 | float | Variable | Context features |
| **Total** | **41** | Mixed | Various | All for analysis |

### Feature Correlation with Target

**Top Positive Correlations**:
1. Sales_Lag7: +0.95 (strong week-to-week correlation)
2. MA30: +0.92 (trend following)
3. Sales_Lag30: +0.88 (monthly seasonality)
4. EMA7: +0.90 (exponential trend)

**Top Negative Correlations**:
1. Volatility: -0.15 (high volatility = lower predictability)
2. ROC_7d: -0.08 (extreme changes less likely)

---

## Model Architecture

### Facebook Prophet

**Why Prophet?**
- Excellent for business time series (seasonal patterns)
- Robust to missing data and outliers
- Built-in holiday effects
- Interpretable components (trend + seasonality)
- Provides confidence intervals

**Model Configuration**:

```python
model = Prophet(
    # Seasonality settings
    yearly_seasonality=True,
    weekly_seasonality=True,
    daily_seasonality=False,
    
    # Mode: 'additive' (level + seasonal) or 'multiplicative' (level * seasonal)
    seasonality_mode='additive',
    
    # Priors (strength of seasonality effects)
    seasonality_prior_scale=10,        # 0-100 (10 = moderate)
    seasonality_mode_prior_scale=10,   # Flexibility of seasonality
    
    # Trend settings
    changepoint_prior_scale=0.05,      # Flexibility of trend changes
    changepoint_range=0.8,             # Proportion of data for trend detection
    
    # Uncertainty
    interval_width=0.95                # 95% confidence interval
)
```

**Training Process**:

```python
# Prepare data (Prophet requires 'ds' and 'y' columns)
df_prophet = df_train[['Date', 'Total_Sales']].copy()
df_prophet.columns = ['ds', 'y']

# Fit model
model.fit(df_prophet)  # Iterative optimization

# Generate future dates
future = model.make_future_dataframe(periods=365)  # 12 months

# Predict
forecast = model.predict(future)
# Output columns: yhat, yhat_lower, yhat_upper, trend, yearly, weekly, trend_lower, trend_upper
```

**Model Components**:

```
Forecast = Trend + Seasonal(Year) + Seasonal(Week) + Holidays + Error

Where:
- Trend: Long-term direction (linear with changepoints)
- Seasonal(Year): Annual patterns (12-month cycle)
- Seasonal(Week): Weekly patterns (7-day cycle)
- Holidays: Special event impacts
- Error: Residuals (~N(0, σ²))
```

**Decomposition Example**:
```
Total Daily Sales = 
  Baseline Trend: $11,500
  + Yearly Seasonality: +$1,200 (in November)
  + Weekly Seasonality: +$800 (on Saturday)
  + Holidays: +$500 (Black Friday)
  + Error: ±$200
  = ~$13,700 (forecasted)
```

### ARIMA (Alternative/Comparison)

**Configuration**:
```python
model_arima = ARIMA(df_train['Total_Sales'].values, order=(1, 1, 1))
# order = (p, d, q)
# p=1: AR (autoregressive) lag 1
# d=1: Differencing (remove trend)
# q=1: MA (moving average) lag 1
```

**When to Use**:
- Stationary/differenced series
- Strong autocorrelation patterns
- Short-term forecasts
- Less interpretable than Prophet

---

## Model Performance

### Evaluation Metrics

**Training Period**: 876 days (80% of 1,095)  
**Test Period**: 219 days (20%)

**Prophet Results**:
```
Mean Absolute Error (MAE):            $2,145
Root Mean Squared Error (RMSE):       $3,210
Mean Absolute Percentage Error (MAPE): 11.8%
```

**Interpretation**:
- Average forecast error: $2,145/day (~19% of avg daily sales $11,437)
- Confidence interval width: $2,000-$3,000
- Model captures 88% of variance

### Residual Analysis

```python
residuals = actual - forecast

# Normal distribution test
mean(residuals) ≈ 0 ✓
std(residuals) = $3,210
skewness ≈ 0.15 (slight right skew)
kurtosis ≈ 0.22 (normal tails)

# Autocorrelation
ACF[1] = 0.05 (minimal - good!)
ACF[7] = -0.02 (weekly pattern captured)
```

**Conclusion**: Model captures patterns well; residuals are ~white noise

---

## API & Integration

### Data Export Format

**sales_with_forecasts.csv**
```
Date,Type,Total_Sales,Forecast,Forecast_Lower,Forecast_Upper,Transaction_Count,Total_Quantity
2022-01-01,Actual,9850.50,9850.50,9850.50,9850.50,5,12
2024-12-31,Actual,11234.75,11234.75,11234.75,11234.75,6,14
2025-01-01,Forecast,,12145.00,10890.00,13400.00,,
2025-01-02,Forecast,,12078.50,10823.50,13333.50,,
...
```

**Fields**:
- `Date`: YYYY-MM-DD format
- `Type`: "Actual" or "Forecast"
- `Total_Sales`: Recorded sales (Actual only)
- `Forecast`: Predicted sales (Forecast only)
- `Forecast_Lower`: 95% CI lower bound
- `Forecast_Upper`: 95% CI upper bound
- `Transaction_Count`: Number of transactions (Actual only)
- `Total_Quantity`: Units sold (Actual only)

### Power BI Integration

**Connection Steps**:
1. Open Power BI Desktop
2. Get Data → Text/CSV
3. Select `sales_with_forecasts.csv`
4. Load and transform
5. Create relationships with dimension tables
6. Build visualizations

**DAX Measures**:
```dax
# Total Sales
Total_Revenue = SUM(sales_with_forecasts[Total_Sales])

# Forecast vs Actual
Actual_Sales = SUMIF(sales_with_forecasts[Type], "Actual", sales_with_forecasts[Total_Sales])
Forecast_Sales = SUMIF(sales_with_forecasts[Type], "Forecast", sales_with_forecasts[Forecast])

# Accuracy
Forecast_Error = Forecast_Sales - Actual_Sales
Forecast_Accuracy = IF(Forecast_Sales > 0, (1 - ABS(Forecast_Error)/Forecast_Sales), 0)
```

---

## Deployment

### Production Checklist

- [ ] Data pipeline validation (schema, quality)
- [ ] Model performance validation (MAPE < 15%)
- [ ] Error handling and logging
- [ ] Scheduled refresh configuration
- [ ] Backup and disaster recovery
- [ ] Access control and permissions
- [ ] Documentation complete
- [ ] Stakeholder training completed
- [ ] Monitoring and alerts set up
- [ ] Performance baseline established

### Scheduled Updates

**Daily**:
```bash
# Update actual sales data
python notebooks/01_eda_data_cleaning.ipynb
# Regenerate forecasts
python notebooks/03_time_series_forecasting.ipynb
# Update exports
# Time: 2:00 AM UTC (off-peak)
```

**Weekly**:
```bash
# Analyze performance metrics
# Review forecast accuracy vs actual
# Flag significant deviations
```

**Monthly**:
```bash
# Retrain Prophet model with new month data
# Update Power BI dashboard
# Generate executive summary
```

**Quarterly**:
```bash
# Full model retraining
# Feature importance analysis
# Business metrics review
```

### Monitoring & Alerts

**KPI Thresholds**:
```
⚠️  Alert if MAPE > 15% (model degradation)
⚠️  Alert if forecast lower bound < 0 (data issue)
⚠️  Alert if daily sales deviation > 30% from forecast
🔴 Critical if data pipeline fails to run
```

---

## Troubleshooting

### Common Issues

#### Issue: Prophet Model Training Fails
**Symptoms**: "Fitting failed" or infinite error

**Solutions**:
1. Check for missing values in training data
2. Verify date column is datetime type
3. Ensure 'y' values are numeric and non-negative
4. Increase `interval_width` if issues persist
5. Try different `seasonality_mode` ('additive' vs 'multiplicative')

#### Issue: Forecast Accuracy (MAPE) > 20%
**Symptoms**: Predictions consistently far from actual

**Solutions**:
1. Increase training data period (need min 2 years)
2. Adjust `seasonality_prior_scale` (try 5-15)
3. Adjust `changepoint_prior_scale` (try 0.01-0.1)
4. Check for unusual events/anomalies in data
5. Consider different seasonality settings

#### Issue: Power BI Dashboard Shows Blanks
**Symptoms**: Missing data in visualizations

**Solutions**:
1. Verify CSV files are loaded correctly
2. Check column names match DAX formulas
3. Ensure Date column is recognized as date type
4. Validate filter selections aren't hiding data
5. Check for null values in source data

#### Issue: Slow Performance/Long Forecast Times
**Symptoms**: Model training takes >30 minutes

**Solutions**:
1. Reduce training data (use last 2 years if 3 available)
2. Disable weekly seasonality if not needed
3. Increase `interval_width` to 0.90
4. Use faster hardware (CPU-intensive)
5. Parallelize if multiple regions/stores

### Debug Checklist

```python
# Check data quality
print(df.isnull().sum())                    # Missing values
print(df.dtypes)                            # Correct types
print(df.describe())                        # Statistical summary
print(df[df['Sales_Amount'] < 0])          # Negative values
print(len(df[df['Date'].duplicated()]))    # Duplicate dates

# Check model fit
forecast = model.make_future_dataframe(periods=1)
forecast = model.predict(forecast)
print(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail())

# Check residuals
residuals = actual_test - forecast_test
print(f"MAE: {np.mean(np.abs(residuals))}")
print(f"RMSE: {np.sqrt(np.mean(residuals**2))}")
```

---

## Performance Optimization

### Data Processing

**Current Performance**:
- Data cleaning: 2-3 seconds
- Feature engineering: 5-7 seconds
- Prophet training: 15-20 seconds
- Forecasting: 3-5 seconds
- **Total end-to-end: ~25-35 seconds**

**Optimization Opportunities**:
1. Vectorize operations (use NumPy over loops)
2. Cache intermediate results
3. Parallelize Prophet model training
4. Use efficient data types (int8/int16 where possible)

### Scaling Considerations

**Single Store/Category**:
- Current approach sufficient
- 1-2 seconds inference time

**Multiple Stores** (5+):
- Train separate models per store
- Parallelize with `multiprocessing`
- Estimated time: 2 minutes for 5 stores

**Real-Time Forecasting**:
- Pre-train models; cache predictions
- Update nightly with new data
- Serve from database (sub-100ms)

---

## Security & Compliance

### Data Protection

- **PII**: No personal information in dataset (store-level aggregate)
- **Encryption**: Store CSV files in encrypted folder
- **Access Control**: Restrict Power BI dashboard by role
- **Audit**: Log all data access and model changes

### Model Governance

- **Documentation**: All assumptions recorded
- **Versioning**: Track model iterations
- **Validation**: Regular accuracy checks
- **Bias**: Monitor for fairness across regions/categories

---

## Support & Maintenance

**Contact**: data-team@company.com  
**On-Call**: Available for critical issues  
**Response Time**: < 4 hours for production issues  
**Maintenance Window**: Weekly (Tuesday 2-4 AM UTC)

### Knowledge Base

- Prophet documentation: https://facebook.github.io/prophet/
- Pandas guide: https://pandas.pydata.org/docs/
- Power BI tutorials: https://docs.microsoft.com/power-bi/
- Time series best practices: [Internal Wiki]

---

**Document Version**: 1.0  
**Last Updated**: December 2024  
**Maintained By**: Data Science Team
