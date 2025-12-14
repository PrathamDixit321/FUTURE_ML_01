# Power BI Dashboard Setup Guide

## 📊 Dashboard Overview

This comprehensive sales forecasting dashboard helps retail businesses visualize historical sales data, analyze trends, and leverage machine learning forecasts to make data-driven decisions.

---

## 🎯 Dashboard Pages & Visualizations

### **Page 1: Executive Summary**

#### Key Metrics (Cards)
- **Total Historical Revenue**: Sum of all sales_with_forecasts (where Type = 'Actual')
- **12-Month Forecast Revenue**: Sum of monthly_forecasts (Forecast_Sales)
- **Average Daily Sales**: Average of daily sales
- **Expected Growth Rate**: Calculated percentage
- **Top Performing Store**: Card showing best store
- **Top Category**: Card showing best product category

#### Visualizations
1. **Sales Trend (Line Chart)**
   - X-axis: Date
   - Y-axis: Total_Sales (split by Type: Actual vs Forecast)
   - Add trend line with confidence interval

2. **Revenue Distribution Pie Charts**
   - By Category (from category_analysis.csv)
   - By Store (from store_analysis.csv)
   - By Region (from region_analysis.csv)

3. **Monthly Comparison (Bar Chart)**
   - X-axis: Year_Month
   - Y-axis: Forecast_Sales
   - Color by performance (good/average/poor)

---

### **Page 2: Historical Analysis**

#### Visualizations
1. **Daily Sales Heatmap**
   - Rows: Day of Week
   - Columns: Week of Year
   - Values: Average Daily Sales
   - Color intensity shows high/low periods

2. **Category Performance Matrix**
   - X-axis: Store
   - Y-axis: Category
   - Size and color: Sales amount
   - Interactive bubbles for detail

3. **Top 10 Store-Category Combinations**
   - Horizontal bar chart
   - Shows highest revenue combinations

4. **Monthly Year-over-Year Comparison**
   - Multi-line chart
   - Compare 2022 vs 2023 vs 2024 by month

---

### **Page 3: Seasonal Patterns & Forecasting**

#### Visualizations
1. **Seasonal Decomposition**
   - Line chart showing:
     - Actual sales (blue)
     - Trend component (red)
     - Seasonality overlay (shaded areas)

2. **Monthly Pattern Analysis**
   - Column chart with 12 months
   - Color gradient: Green (high) to Red (low)
   - Add average line

3. **Forecast vs Actual (Detailed)**
   - Combination chart:
     - Bars for Actual (last 6 months)
     - Line for Forecast (next 12 months)
     - Shaded CI band

4. **Peak Season Identifier**
   - Table showing:
     - Month
     - Average Sales
     - Seasonality Index
     - Recommendation

---

### **Page 4: Regional & Store Deep Dive**

#### Visualizations
1. **Regional Performance Scorecard**
   - KPI tiles for each region:
     - Total Sales
     - Growth %
     - Store Count
     - Status indicator

2. **Store Comparison Matrix**
   - Create matrix with:
     - Rows: Store names
     - Columns: Category
     - Values: Sales $
     - Conditional formatting

3. **Regional Sales Map** (if possible)
   - Geographic visualization of regions
   - Bubble size = Sales
   - Color = Growth rate

4. **Store Performance Trend**
   - Line chart for each store
   - Track over historical period
   - Benchmark against average

---

### **Page 5: Key Insights & Recommendations**

#### Visualizations
1. **Top 5 Insights (Text Cards)**
   - Highest Revenue Category
   - Fastest Growing Category
   - Best Performing Store
   - Peak Selling Period
   - Growth Forecast

2. **Action Items (Visual List)**
   - KPI indicators showing:
     - Inventory Recommendations
     - Marketing Focus Areas
     - Store Optimization Needs
     - Seasonal Adjustments

3. **Forecast Confidence**
   - Gauge chart showing model confidence
   - Breakdown of forecast reliability by period

4. **Risk Indicators**
   - Cards highlighting:
     - Underperforming stores
     - Declining categories
     - Inventory risks
     - Demand volatility

---

## 🔌 Data Model Setup

### Required Data Files

1. **sales_with_forecasts.csv**
   - Main dataset with actual and forecast values
   - Fields: Date, Type, Total_Sales, Forecast, Forecast_Lower, Forecast_Upper

2. **monthly_forecasts.csv**
   - Monthly-level forecasts
   - Fields: YearMonth, Forecast_Sales, Forecast_Lower, Forecast_Upper

3. **daily_forecasts.csv**
   - Daily forecast details
   - Fields: Date, Forecast, Forecast_Lower, Forecast_Upper, Trend, Yearly_Seasonality

4. **kpi_summary.csv**
   - Key performance indicators
   - Supports summary page metrics

5. **category_analysis.csv**
   - Category performance breakdown
   - For distribution charts

6. **store_analysis.csv**
   - Store performance metrics
   - For store comparisons

7. **region_analysis.csv**
   - Regional performance
   - For geographic analysis

### Data Model Relationships

```
sales_with_forecasts (Main Fact Table)
├── Linked to dates via Date column
├── Linked to categories via implicit relationship
└── Contains both actual and forecast data

monthly_forecasts (Forecast Aggregation)
├── Linked to sales_with_forecasts for trends
└── Supports monthly-level analysis

Category/Store/Region Analysis (Dimension Tables)
├── Support drill-down analysis
└── Enable comparative visualizations
```

### Calculated Columns & Measures

**In Power BI, create these measures:**

```DAX
# Revenue Metrics
Total_Sales = SUM(sales_with_forecasts[Total_Sales])
Historical_Sales = SUMIF(sales_with_forecasts, sales_with_forecasts[Type], "Actual")
Forecast_Sales = SUMIF(sales_with_forecasts, sales_with_forecasts[Type], "Forecast")

# Growth Metrics
YoY_Growth = DIVIDE([Total_Sales This Year], [Total_Sales Last Year], 0) - 1
MoM_Growth = DIVIDE([Total_Sales This Month], [Total_Sales Last Month], 0) - 1

# Average Metrics
Avg_Daily_Sales = AVERAGEX(VALUES(sales_with_forecasts[Date]), [Total_Sales])
Avg_Transaction = DIVIDE([Total_Sales], COUNTA(sales_with_forecasts[Transaction_Count]), 0)

# Trend Metrics
Trend_Direction = IF([MoM_Growth] > 0, "↑", IF([MoM_Growth] < 0, "↓", "→"))
Forecast_Accuracy = CALCULATE([Total_Sales], sales_with_forecasts[Type] = "Actual") / 
                    CALCULATE([Total_Sales], sales_with_forecasts[Type] = "Forecast")

# Seasonal Metrics
Days_to_Peak = CALCULATE(DATEDIFF(TODAY(), MAX(sales_with_forecasts[Date]), DAY))
Peak_Season_Indicator = IF(MONTH(TODAY()) IN {10, 11, 12}, "High", "Low")
```

---

## 🎨 Design Best Practices

### Color Scheme
- **Primary**: Blue (#1F77B4) for actuals
- **Secondary**: Orange (#FF7F0E) for forecasts
- **Success**: Green (#2CA02C) for positive growth
- **Warning**: Red (#D62728) for concerns
- **Neutral**: Gray (#7F7F7F) for trends

### Layout Guidelines
1. **Top Section**: High-level KPIs and summary metrics
2. **Middle Section**: Detailed visualizations and trends
3. **Bottom Section**: Drill-down data and supporting details
4. **Right Panel**: Filters and slicers for interactivity

### Interactivity Features
- **Slicers**: Date range, Category, Store, Region
- **Cross-filtering**: Click any visual to filter others
- **Drill-through**: From summary to detailed analysis
- **Bookmarks**: Save views for quick access

---

## 📋 Recommended Slicers

1. **Date Range Slicer**
   - Type: Date picker or range slider
   - Default: Last 12 months

2. **Category Slicer**
   - Type: Dropdown/checkbox
   - Options: All categories or specific selections

3. **Store Slicer**
   - Type: Dropdown/checkbox
   - Options: All stores or regional groupings

4. **Region Slicer**
   - Type: Dropdown
   - Options: All regions or all

5. **Forecast Type Slicer**
   - Type: Radio buttons
   - Options: Actual | Forecast | Both

---

## 📈 Dashboard Workflow

### User Journey

```
1. Executive Summary
   ↓
2. Select Time Period (Date Slicer)
   ↓
3. View Key Metrics & Trends
   ↓
4. Drill into Regional/Store Performance
   ↓
5. Analyze Category Breakdown
   ↓
6. Review Seasonal Patterns & Forecast
   ↓
7. Check Recommendations & Action Items
```

---

## 🔄 Refresh & Maintenance

### Data Refresh Schedule
- **Daily**: Update sales_with_forecasts.csv with new transactions
- **Weekly**: Regenerate forecasts using latest Prophet model
- **Monthly**: Update monthly_forecasts.csv and analysis files
- **Quarterly**: Retrain forecasting model with new data

### Power BI Configuration
1. **Scheduled Refresh**: Set to run at 2 AM UTC daily
2. **Gateway Configuration**: If using on-premises data
3. **Row-Level Security**: Restrict by store/region if needed
4. **Mobile Optimization**: Ensure all visuals are responsive

---

## 📊 Visualization Examples

### Card/KPI Visualizations
```
┌─────────────────────────┐
│  Total Revenue          │
│   $12,543,897.50        │
│   ↑ 15.2% vs Last Year   │
└─────────────────────────┘
```

### Combo Chart (Actual vs Forecast)
```
   Bars = Actuals (blue)
   Line = Forecast (orange)
   Shaded area = Confidence interval
```

### Heat Map
```
   Rows: Days of week
   Cols: Weeks
   Color intensity: Sales volume
   Darker = Higher sales
```

---

## 🎯 Key Metrics to Monitor

1. **Sales Velocity**
   - Daily trend
   - Week-over-week growth
   - Month-over-month comparison

2. **Forecast Accuracy**
   - Actual vs Forecast deviation
   - Confidence interval width
   - Seasonal adjustment effectiveness

3. **Segment Performance**
   - Top 3 categories
   - Best/worst stores
   - Regional leaders

4. **Seasonal Indicators**
   - Days until peak season
   - Current seasonality factor
   - Inventory readiness

---

## 🚀 Implementation Checklist

- [ ] Load all CSV files into Power BI
- [ ] Create relationships between tables
- [ ] Define all DAX measures
- [ ] Build Page 1: Executive Summary
- [ ] Build Page 2: Historical Analysis
- [ ] Build Page 3: Seasonal Patterns
- [ ] Build Page 4: Regional Deep Dive
- [ ] Build Page 5: Insights & Recommendations
- [ ] Add slicers and filters
- [ ] Apply conditional formatting
- [ ] Test cross-filtering
- [ ] Configure scheduled refresh
- [ ] Set up alerts for KPI thresholds
- [ ] Create mobile-optimized layout
- [ ] Document dashboard usage
- [ ] Share with stakeholders

---

## 📞 Support & Troubleshooting

### Common Issues

**Issue**: Forecast not showing up
- **Solution**: Ensure Type = 'Forecast' filter is applied; check date range

**Issue**: Seasonal patterns unclear
- **Solution**: Increase time period to 12+ months; check if all years are included

**Issue**: Store comparison unfair
- **Solution**: Apply regional filter; normalize by store size if available

**Issue**: Slow dashboard performance
- **Solution**: Reduce time period; create separate dashboards by region/store

---

## 📚 Additional Resources

### Files in Project
- `notebooks/00_generate_sample_data.ipynb` - Data generation
- `notebooks/01_eda_data_cleaning.ipynb` - Data exploration
- `notebooks/02_feature_engineering.ipynb` - Feature creation
- `notebooks/03_time_series_forecasting.ipynb` - Model training
- `notebooks/04_business_analytics.ipynb` - Analysis & insights

### Data Exports
- `exports/sales_with_forecasts.csv` - **Primary dashboard data**
- `exports/monthly_forecasts.csv` - Monthly aggregation
- `exports/daily_forecasts.csv` - Daily detail
- `exports/kpi_summary.csv` - Summary metrics
- `exports/category_analysis.csv` - Category breakdown
- `exports/store_analysis.csv` - Store performance
- `exports/region_analysis.csv` - Regional data

---

## 🎓 Learning Resources

1. **Time Series Forecasting**
   - Facebook Prophet Documentation
   - ARIMA Model Fundamentals
   - Seasonal Pattern Analysis

2. **Power BI Skills**
   - DAX Fundamentals
   - Data Modeling Best Practices
   - Advanced Visualizations

3. **Business Intelligence**
   - KPI Definition & Tracking
   - Dashboard Design Principles
   - Storytelling with Data

---

**Last Updated**: December 2024
**Version**: 1.0
**Maintained By**: Data Analytics Team
