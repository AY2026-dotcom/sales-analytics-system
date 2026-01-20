import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


import pandas as pd
import numpy as np
from datetime import datetime


from utils.file_handler import (
    read_sales_data,
    write_report,
    save_cleaned_data,
    parse_transactions,
    validate_and_filter
)

from utils.data_processor import (
    validate_and_clean,
    analyze_sales
)

from utils.api_handler import (
    fetch_all_products,
    create_product_mapping,
    enrich_sales_data,
    fetch_exchange_rates
)

from utils.report_generator import generate_sales_report


def generate_summary_report(analysis, invalid_count, rates):
    report = []
    report.append("=" * 75)
    report.append("SALES DATA ANALYTICS REPORT")
    report.append("=" * 75)
    report.append(f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("")

    report.append("OVERALL SUMMARY")
    report.append("-" * 75)
    report.append(f"Total Revenue: ${analysis['total_revenue']:,.2f}")
    report.append(f"Total Transactions: {analysis['transaction_count']}")
    report.append(f"Average Order Value: ${analysis['avg_transaction']:,.2f}")
    report.append("")

    if rates:
        report.append("REVENUE (MULTI-CURRENCY)")
        report.append("-" * 75)
        rev = analysis['total_revenue']
        report.append(f"USD: ${rev:,.2f}")
        report.append(f"EUR: €{rev * rates['EUR']:,.2f}")
        report.append(f"GBP: £{rev * rates['GBP']:,.2f}")
        report.append(f"INR: ₹{rev * rates['INR']:,.2f}")
        report.append("")

    report.append("REGION-WISE PERFORMANCE")
    report.append("-" * 75)
    for region, revenue in sorted(
        analysis['region_sales'].items(),
        key=lambda x: x[1],
        reverse=True
    ):
        report.append(f"{region:15s} ${revenue:,.2f}")

    report.append("=" * 75)
    return "\n".join(report)


def generate_invalid_report(invalid_df):
    report = []
    report.append("=" * 75)
    report.append("INVALID RECORDS REPORT")
    report.append("=" * 75)
    report.append(f"Total Invalid Records: {len(invalid_df)}")
    return "\n".join(report)


def main_task1_pipeline():
    print("Running Task 1 pipeline (parsing & validation only)")

    raw_lines = read_sales_data("data/sales_data.txt")
    transactions = parse_transactions(raw_lines)
    valid_txns, invalid_count, _ = validate_and_filter(transactions)

    print(f"Valid: {len(valid_txns)}, Invalid: {invalid_count}")


def main():
    print("\n" + "=" * 75)
    print("SALES DATA ANALYTICS SYSTEM")
    print("=" * 75)

    # STEP 1: Read data
    df = read_sales_data("data/sales_data.txt")
    if df.empty:
        print("No data found.")
        return

    # STEP 2: Clean & validate
    valid_df, invalid_df = validate_and_clean(df)
    if valid_df.empty:
        print("No valid records.")
        return

    # STEP 3: API – Fetch products
    api_products = fetch_all_products()
    product_mapping = create_product_mapping(api_products)

    # STEP 4: API – Enrich sales data
    enriched_transactions = enrich_sales_data(
        valid_df.to_dict(orient="records"),
        product_mapping
    )
    enriched_df = pd.DataFrame(enriched_transactions)

    # STEP 5: API – Exchange rates
    rates = fetch_exchange_rates()

    # STEP 6: Analysis
    analysis = analyze_sales(enriched_df)

    # STEP 7: Report generation
    os.makedirs("output", exist_ok=True)

    summary_report = generate_summary_report(
        analysis,
        len(invalid_df),
        rates
    )
    write_report("output/sales_summary_report.txt", summary_report)

    invalid_report = generate_invalid_report(invalid_df)
    write_report("output/invalid_records_report.txt", invalid_report)

    generate_sales_report(
        valid_df.to_dict(orient="records"),
        enriched_transactions
    )

    save_cleaned_data("output/cleaned_sales_data.txt", enriched_df)
    enriched_df.to_csv("output/cleaned_sales_data.csv", index=False)

    print("Processing complete!")


if __name__ == "__main__":
    main()
