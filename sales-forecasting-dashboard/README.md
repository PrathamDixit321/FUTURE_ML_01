# AI-Powered Sales Forecasting Dashboard

A comprehensive retail sales forecasting solution combining Python machine learning models with Power BI visualization.

## 📁 Project Structure

```
sales-forecasting-dashboard/
├── data/                          # Raw and processed datasets
│   ├── sales_historical.csv       # Historical transaction data
│   ├── sales_processed.csv        # Cleaned and engineered data
│   └── forecasts.csv              # Model predictions
├── notebooks/                     # Jupyter notebooks
│   ├── 01_eda_data_cleaning.ipynb        # Exploratory analysis & cleaning
│   ├── 02_feature_engineering.ipynb      # Feature creation & preprocessing
│   ├── 03_time_series_forecasting.ipynb  # Model training & prediction
│   └── 04_analysis_summary.ipynb         # Results & recommendations
├── models/                        # Saved model artifacts
│   ├── prophet_model.pkl
│   └── forecast_results.pkl
├── exports/                       # Power BI ready datasets
│   ├── sales_with_forecasts.csv   # Combined actual + forecast data
│   └── kpi_summary.csv            # Key metrics for dashboard
├── docs/                          # Documentation
│   ├── business_recommendations.md
│   └── technical_documentation.md
└── README.md
```

## 🎯 Project Objectives

- **Data Preparation**: Clean and structure historical retail data
- **Feature Engineering**: Create seasonal indicators, trends, and anomaly flags
- **Time Series Forecasting**: Train Prophet/ARIMA models on sales data
- **Dashboard Creation**: Build interactive Power BI visualizations
- **Business Insights**: Provide actionable recommendations based on analysis

## 📊 Key Features

✅ Sales trend visualization (actual vs. forecasted)  
✅ Monthly & yearly comparisons  
✅ Store, category, and region filters  
✅ Top-selling items & seasonality analysis  
✅ KPI cards & decision-making insights  

## 🛠️ Tools Used

- **Python**: Data processing & ML modeling
- **Jupyter Notebook**: Interactive analysis workflow
- **Pandas & NumPy**: Data manipulation
- **Facebook Prophet**: Time series forecasting
- **Scikit-learn**: Feature engineering & preprocessing
- **Power BI**: Interactive dashboarding

## 🚀 Workflow

1. **Exploratory Data Analysis (EDA)**: Understand data patterns and quality
2. **Data Cleaning**: Handle missing values, outliers, and inconsistencies
3. **Feature Engineering**: Create domain-specific features for forecasting
4. **Model Training**: Implement Prophet/ARIMA forecasting models
5. **Validation & Export**: Evaluate forecasts and export for BI
6. **Dashboard Building**: Create interactive visualizations in Power BI
7. **Business Recommendations**: Document insights and actions

## 📈 Expected Outcomes

- Accurate 6-12 month sales forecasts
- Identification of seasonal patterns and trends
- Recognition of top performers and underperformers
- Data-driven recommendations for inventory and marketing
- Interactive dashboard for stakeholder decision-making

## 💡 Skills Developed

- Time series forecasting with statistical & ML models
- End-to-end data science workflow
- Business analytics & storytelling
- Power BI dashboard development
- Data-driven decision making
