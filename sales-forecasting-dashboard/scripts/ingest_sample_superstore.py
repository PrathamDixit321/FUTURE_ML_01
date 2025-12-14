import argparse
import os 
from pathlib import Path
import pandas as pd


def safe_mkdir(path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)


def ingest(input_csv: str, out_dir: str):
    src = Path(input_csv)
    out = Path(out_dir)
    if not src.exists():
        raise FileNotFoundError(f"Input file not found: {src}")

    try:
        df = pd.read_csv(src, parse_dates=["Order Date"], dayfirst=False, infer_datetime_format=True)
    except UnicodeDecodeError:
        # Try common Windows encoding for legacy CSVs
        df = pd.read_csv(src, encoding='cp1252', parse_dates=["Order Date"], dayfirst=False)

    # Normalize column names
    df.columns = [c.strip() for c in df.columns]

    # Required mappings (from Superstore-like schema)
    # Order Date -> Date, Sales -> Sales, Quantity -> Quantity
    if "Order Date" not in df.columns or "Sales" not in df.columns:
        raise ValueError("Expected columns 'Order Date' and 'Sales' in the input CSV")

    df = df.rename(columns={"Order Date": "Date", "Sales": "Sales", "Quantity": "Quantity"})

    # Use City as Store (if present), otherwise fill with 'All'
    if "City" in df.columns:
        df["Store"] = df["City"]
    else:
        df["Store"] = "All"

    # Region and Category available in the Superstore dataset
    if "Region" not in df.columns:
        df["Region"] = "Unknown"

    if "Category" not in df.columns:
        df["Category"] = "Unknown"

    # Basic cleaning: drop rows without Date or Sales
    cleaned = df.dropna(subset=["Date", "Sales"]).copy()

    # Ensure numeric types
    cleaned["Sales"] = pd.to_numeric(cleaned["Sales"], errors="coerce")
    if "Quantity" in cleaned.columns:
        cleaned["Quantity"] = pd.to_numeric(cleaned["Quantity"], errors="coerce").fillna(0).astype(int)
    else:
        cleaned["Quantity"] = 0

    cleaned = cleaned.dropna(subset=["Sales"])  # drop rows where Sales couldn't be converted

    # Output paths
    data_dir = Path("data")
    safe_mkdir(data_dir / "." )

    sales_historical = data_dir / "sales_historical.csv"
    sales_cleaned = data_dir / "sales_cleaned.csv"
    sales_daily = data_dir / "sales_daily.csv"
    sales_monthly = data_dir / "sales_monthly.csv"

    # Save historical (a cleaned copy of the original with a consistent date column)
    cleaned.to_csv(sales_historical, index=False)

    # Save cleaned subset used by notebooks
    cleaned.to_csv(sales_cleaned, index=False)

    # Daily aggregation (company-wide)
    daily = (
        cleaned.assign(Date=cleaned["Date"].dt.normalize())
        .groupby("Date")
        .agg(
            Total_Sales=("Sales", "sum"),
            Total_Quantity=("Quantity", "sum"),
            Transactions=("Order ID", "nunique") if "Order ID" in cleaned.columns else ("Sales", "count"),
        )
        .reset_index()
    )
    daily.to_csv(sales_daily, index=False)

    # Monthly aggregation
    monthly = (
        cleaned.assign(YearMonth=cleaned["Date"].dt.to_period("M").astype(str))
        .groupby("YearMonth")
        .agg(
            Monthly_Sales=("Sales", "sum"),
            Monthly_Quantity=("Quantity", "sum"),
        )
        .reset_index()
    )
    monthly.to_csv(sales_monthly, index=False)

    print(f"Wrote: {sales_historical} ({len(cleaned)} rows)")
    print(f"Wrote: {sales_cleaned}")
    print(f"Wrote: {sales_daily} ({len(daily)} rows)")
    print(f"Wrote: {sales_monthly} ({len(monthly)} rows)")


def main():
    parser = argparse.ArgumentParser(description="Ingest Superstore CSV into project data/ files")
    parser.add_argument("--input", default=r"data/Sample - Superstore.csv", help="Path to the input CSV")
    parser.add_argument("--out", default="data", help="Output directory (defaults to data/)")
    args = parser.parse_args()
    ingest(args.input, args.out)


if __name__ == "__main__":
    main()
