"""Train Prophet on daily sales and export forecast CSVs for Power BI.

Writes to: exports/sales_with_forecasts.csv, exports/daily_forecasts.csv, exports/monthly_forecasts.csv
"""
from pathlib import Path
import pandas as pd
import numpy as np
from prophet import Prophet


def main():
    data_dir = Path('data')
    exports_dir = Path('exports')
    exports_dir.mkdir(parents=True, exist_ok=True)

    df_daily = pd.read_csv(data_dir / 'sales_daily.csv', parse_dates=['Date'])
    df_daily = df_daily.sort_values('Date').reset_index(drop=True)

    # Ensure column names expected by the script
    if 'Transactions' in df_daily.columns:
        df_daily = df_daily.rename(columns={'Transactions': 'Transaction_Count'})
    if 'Total_Quantity' not in df_daily.columns and 'Total_Quantity' in df_daily.columns:
        pass

    # Prepare for Prophet
    df_prophet = df_daily[['Date', 'Total_Sales']].rename(columns={'Date': 'ds', 'Total_Sales': 'y'})

    # Train/test split (80/20)
    train_size = int(len(df_prophet) * 0.8)
    df_train = df_prophet.iloc[:train_size]

    model = Prophet(yearly_seasonality=True, weekly_seasonality=True, daily_seasonality=False,
                    seasonality_mode='additive', interval_width=0.95)
    model.fit(df_train)

    # Forecast next 365 days
    future = model.make_future_dataframe(periods=365)
    forecast = model.predict(future)

    # Prepare exports
    last_training_date = df_train['ds'].max()
    forecast_future = forecast[forecast['ds'] > last_training_date].copy()
    forecast_future_out = forecast_future[['ds', 'yhat', 'yhat_lower', 'yhat_upper', 'trend']].rename(
        columns={'ds': 'Date', 'yhat': 'Forecast', 'yhat_lower': 'Forecast_Lower', 'yhat_upper': 'Forecast_Upper', 'trend': 'Trend'})

    # Monthly aggregation
    forecast_future_out['YearMonth'] = forecast_future_out['Date'].dt.to_period('M').astype(str)
    monthly = forecast_future_out.groupby('YearMonth').agg({
        'Forecast': 'sum', 'Forecast_Lower': 'sum', 'Forecast_Upper': 'sum'
    }).reset_index().rename(columns={'Forecast': 'Forecast_Sales'})

    # Combined actual + forecast for Power BI
    df_actual = df_daily.copy()
    # normalize columns
    df_actual = df_actual.rename(columns={'Date': 'Date', 'Total_Sales': 'Total_Sales'})
    df_actual['Type'] = 'Actual'
    df_actual['Forecast'] = df_actual['Total_Sales']
    df_actual['Forecast_Lower'] = df_actual['Total_Sales']
    df_actual['Forecast_Upper'] = df_actual['Total_Sales']

    df_forecast = forecast_future_out.copy()
    df_forecast['Type'] = 'Forecast'
    df_forecast['Total_Sales'] = df_forecast['Forecast']
    df_forecast['Transaction_Count'] = np.nan
    df_forecast['Total_Quantity'] = np.nan

    df_powerbi = pd.concat([
        df_actual[['Date', 'Type', 'Total_Sales', 'Forecast', 'Forecast_Lower', 'Forecast_Upper', 'Transaction_Count', 'Total_Quantity']],
        df_forecast[['Date', 'Type', 'Total_Sales', 'Forecast', 'Forecast_Lower', 'Forecast_Upper', 'Transaction_Count', 'Total_Quantity']]
    ], ignore_index=True).sort_values('Date').reset_index(drop=True)

    # Export
    df_powerbi.to_csv(exports_dir / 'sales_with_forecasts.csv', index=False)
    forecast_future_out.to_csv(exports_dir / 'daily_forecasts.csv', index=False)
    monthly.to_csv(exports_dir / 'monthly_forecasts.csv', index=False)

    print('Exports written to', exports_dir)


if __name__ == '__main__':
    main()
