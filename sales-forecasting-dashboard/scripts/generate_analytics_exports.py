"""Compute KPIs and segment analyses and write exports for Power BI.

Writes to: exports/kpi_summary.csv, exports/category_analysis.csv, exports/store_analysis.csv, exports/region_analysis.csv
"""
from pathlib import Path
import pandas as pd


def main():
    data_dir = Path('data')
    exports_dir = Path('exports')
    exports_dir.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(data_dir / 'sales_historical.csv', parse_dates=['Date'])

    # Basic KPIs
    total_revenue = df['Sales'].sum()
    avg_daily = df.groupby(df['Date'].dt.normalize()).agg({'Sales': 'sum'})['Sales'].mean()
    total_transactions = df['Order ID'].nunique() if 'Order ID' in df.columns else len(df)
    avg_transaction = df['Sales'].sum() / total_transactions if total_transactions else 0

    kpis = {
        'Total_Revenue': [total_revenue],
        'Average_Daily_Sales': [avg_daily],
        'Total_Transactions': [total_transactions],
        'Average_Transaction_Value': [avg_transaction]
    }
    kpi_df = pd.DataFrame(kpis)
    kpi_df.to_csv(exports_dir / 'kpi_summary.csv', index=False)

    # Category analysis
    if 'Category' in df.columns:
        cat = df.groupby('Category').agg(Total_Sales=('Sales', 'sum'), Total_Quantity=('Quantity', 'sum')).reset_index()
        cat.to_csv(exports_dir / 'category_analysis.csv', index=False)

    # Store (City) analysis
    if 'City' in df.columns:
        store = df.groupby('City').agg(Total_Sales=('Sales', 'sum'), Transactions=('Order ID', 'nunique')).reset_index()
        store.to_csv(exports_dir / 'store_analysis.csv', index=False)

    # Region analysis
    if 'Region' in df.columns:
        region = df.groupby('Region').agg(Total_Sales=('Sales', 'sum')).reset_index()
        region.to_csv(exports_dir / 'region_analysis.csv', index=False)

    print('Analytics exports written to', exports_dir)


if __name__ == '__main__':
    main()
