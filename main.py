import os
import pandas as pd
import numpy as np
from datetime import datetime
from utils.file_handler import read_sales_data, write_report, save_cleaned_data
from utils.data_processor import validate_and_clean, analyze_sales
from utils.api_handler import enrich_with_categories, fetch_exchange_rates


def generate_summary_report(analysis, invalid_count, rates):
    """
    Generate comprehensive summary report
    """
    report = []
    report.append("=" * 75)
    report.append("SALES DATA ANALYTICS REPORT")
    report.append("=" * 75)
    report.append(f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("")
    
    # Data Quality Section
    report.append("DATA QUALITY SUMMARY")
    report.append("-" * 75)
    report.append(f"Valid Transactions Processed: {analysis['transaction_count']}")
    report.append(f"Invalid Records Rejected: {invalid_count}")
    report.append("")
    
    # Revenue Analysis
    report.append("REVENUE ANALYSIS")
    report.append("-" * 75)
    report.append(f"Total Revenue: ${analysis['total_revenue']:,.2f}")
    report.append(f"Average Transaction: ${analysis['avg_transaction']:,.2f}")
    report.append(f"Median Transaction: ${analysis['median_transaction']:,.2f}")
    report.append(f"Standard Deviation: ${analysis['std_dev']:,.2f}")
    report.append(f"Minimum Transaction: ${analysis['min_transaction']:,.2f}")
    report.append(f"Maximum Transaction: ${analysis['max_transaction']:,.2f}")
    report.append(f"Total Units Sold: {analysis['total_units']:,.0f}")
    report.append("")
    
    # Currency Conversion
    if rates:
        report.append("REVENUE IN MULTIPLE CURRENCIES")
        report.append("-" * 75)
        rev = analysis['total_revenue']
        report.append(f"USD: ${rev:,.2f}")
        report.append(f"EUR: €{rev * rates['EUR']:,.2f}")
        report.append(f"GBP: £{rev * rates['GBP']:,.2f}")
        report.append(f"INR: ₹{rev * rates['INR']:,.2f}")
        report.append(f"Exchange rates as of: {rates['date']}")
        report.append("")
    
    # Regional Performance
    report.append("REGIONAL SALES PERFORMANCE")
    report.append("-" * 75)
    total = analysis['total_revenue']
    sorted_regions = sorted(analysis['region_sales'].items(), 
                           key=lambda x: x[1], reverse=True)
    
    for region, revenue in sorted_regions:
        percentage = (revenue / total) * 100
        report.append(f"{region:15s} ${revenue:15,.2f}  ({percentage:5.1f}%)")
    report.append("")
    
    # Top Products
    report.append("TOP 5 PRODUCTS BY REVENUE")
    report.append("-" * 75)
    for rank, (product, data) in enumerate(analysis['top_products'], 1):
        report.append(f"{rank}. {product}")
        report.append(f"   Revenue: ${data['revenue']:,.2f}")
        report.append(f"   Units Sold: {data['units']:,.0f}")
        report.append("")
    
    # Top Customers
    report.append("TOP 5 CUSTOMERS BY SPENDING")
    report.append("-" * 75)
    for rank, (customer, spending) in enumerate(analysis['top_customers'], 1):
        report.append(f"{rank}. Customer {customer}: ${spending:,.2f}")
    report.append("")
    
    report.append("=" * 75)
    report.append("Analysis powered by Pandas and NumPy")
    report.append("=" * 75)
    
    return '\n'.join(report)


def generate_invalid_report(invalid_df):
    """
    Generate report for invalid records
    """
    report = []
    report.append("=" * 75)
    report.append("INVALID RECORDS REPORT")
    report.append("=" * 75)
    report.append(f"Total Invalid Records: {len(invalid_df)}")
    report.append("")
    
    for idx, (_, record) in enumerate(invalid_df.iterrows(), 1):
        report.append(f"Invalid Record #{idx}")
        report.append(f"Transaction ID: {record.get('TransactionID', 'N/A')}")
        report.append(f"Rejection Reason: {record.get('Reason', 'Unknown')}")
        report.append(f"Product: {record.get('ProductName', 'N/A')}")
        report.append(f"Customer: {record.get('CustomerID', 'N/A')}")
        report.append("-" * 75)
    
    return '\n'.join(report)

def main():
    """
    Main function using new Task functions
    """
    print("\n" + "=" * 75)
    print("SALES DATA ANALYTICS SYSTEM")
    print("Enhanced with Tasks 1.1, 1.2, and 1.3")
    print("=" * 75)
    print()
    
    # Import the new functions
    from utils.file_handler import read_sales_data as read_raw
    from utils.file_handler import parse_transactions, validate_and_filter
    
    # Task 1.1: Read raw data
    print("TASK 1.1: Reading raw sales data...")
    raw_lines = read_raw('data/sales_data.txt')
    
    if not raw_lines:
        print("ERROR: Could not read data file")
        return
    
    # Task 1.2: Parse transactions
    print("\nTASK 1.2: Parsing transactions...")
    transactions_list = parse_transactions(raw_lines)
    
    if not transactions_list:
        print("ERROR: No transactions parsed")
        return
    
    # Task 1.3: Validate and filter
    print("\nTASK 1.3: Validating and filtering...")
    valid_transactions, invalid_count, filter_summary = validate_and_filter(
        transactions_list
    )
    
    # Convert list of dicts to DataFrame for further processing
    import pandas as pd
    df = pd.DataFrame(valid_transactions)
    
    # Continue with existing pandas/numpy analysis...
    # (rest of your existing main.py code continues here)
    
def main():
    """
    Main function - orchestrates the entire analytics pipeline
    """
    print("\n" + "=" * 75)
    print("SALES DATA ANALYTICS SYSTEM")
    print("Powered by Pandas and NumPy")
    print("=" * 75)
    print()
    
    # Step 1: Read data
    print("STEP 1: Reading Sales Data")
    print("-" * 75)
    df = read_sales_data('data/sales_data.txt')
    
    if df.empty:
        print("ERROR: No data to process. Exiting.")
        return
    
    # Step 2: Clean and validate
    print("STEP 2: Data Cleaning and Validation")
    print("-" * 75)
    valid_df, invalid_df = validate_and_clean(df)
    
    if valid_df.empty:
        print("ERROR: No valid transactions found. Exiting.")
        return
    
    # Step 3: Enrich with categories
    print("STEP 3: Data Enrichment")
    print("-" * 75)
    enriched_df = enrich_with_categories(valid_df)
    
    # Step 4: Fetch exchange rates
    print("STEP 4: API Integration")
    print("-" * 75)
    rates = fetch_exchange_rates()
    
    # Step 5: Perform analysis
    print("STEP 5: Data Analysis")
    print("-" * 75)
    analysis = analyze_sales(enriched_df)
    
    # Step 6: Generate reports
    print("STEP 6: Report Generation")
    print("-" * 75)
    
    # Create output directory
    os.makedirs('output', exist_ok=True)
    
    # Generate and save summary report
    summary = generate_summary_report(analysis, len(invalid_df), rates)
    write_report('output/sales_summary_report.txt', summary)
    
    # Generate and save invalid records report
    if not invalid_df.empty:
        invalid_report = generate_invalid_report(invalid_df)
        write_report('output/invalid_records_report.txt', invalid_report)
    
    # Save cleaned data (pipe-delimited)
    save_cleaned_data('output/cleaned_sales_data.txt', enriched_df)
    
    # Bonus: Save as CSV for easy viewing in Excel
    enriched_df.to_csv('output/cleaned_sales_data.csv', index=False)
    print("Saved: output/cleaned_sales_data.csv")
    
    # Final summary
    print()
    print("=" * 75)
    print("PROCESSING COMPLETE!")
    print("=" * 75)
    print(f"Valid Transactions: {len(valid_df)}")
    print(f"Invalid Records: {len(invalid_df)}")
    print(f"Total Revenue: ${analysis['total_revenue']:,.2f}")
    print(f"Average Transaction: ${analysis['avg_transaction']:,.2f}")
    print()
    print("Generated Reports:")
    print("  • output/sales_summary_report.txt")
    print("  • output/invalid_records_report.txt")
    print("  • output/cleaned_sales_data.txt")
    print("  • output/cleaned_sales_data.csv")
    print("=" * 75)
    print()


if __name__ == "__main__":
    main()