"""
Generate comprehensive analysis report using Task 2 functions
Complete version with alternative import method
"""

import sys
import os
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.file_handler import read_sales_data, parse_transactions, validate_and_filter
from utils.data_processor import (
    calculate_total_revenue,
    region_wise_sales,
    top_selling_products,
    customer_analysis,
    daily_sales_trend,
    find_peak_sales_day,
    low_performing_products
)


def generate_comprehensive_report():
    """Generate and save comprehensive analysis report"""
    
    # Load data
    print("\n" + "=" * 80)
    print("GENERATING COMPREHENSIVE ANALYSIS REPORT")
    print("=" * 80)
    print("\nLoading and processing data...")
    
    raw_lines = read_sales_data('data/sales_data.txt')
    
    if not raw_lines:
        print("ERROR: Could not read data file")
        return None
    
    transactions = parse_transactions(raw_lines)
    
    if not transactions:
        print("ERROR: Could not parse transactions")
        return None
    
    valid_transactions, invalid_count, summary = validate_and_filter(transactions)
    
    if not valid_transactions:
        print("ERROR: No valid transactions found")
        return None
    
    print(f"Data loaded: {len(valid_transactions)} valid transactions")
    print("Generating report...\n")
    
    # Start building report
    report_lines = []
    report_lines.append("=" * 80)
    report_lines.append("COMPREHENSIVE SALES ANALYSIS REPORT")
    report_lines.append("=" * 80)
    report_lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report_lines.append(f"Total Valid Transactions: {len(valid_transactions)}")
    report_lines.append(f"Invalid Transactions: {invalid_count}")
    report_lines.append("")
    
    # ========================================================================
    # Section 1: Revenue Summary
    # ========================================================================
    report_lines.append("=" * 80)
    report_lines.append("1. REVENUE SUMMARY")
    report_lines.append("=" * 80)
    
    total_revenue = calculate_total_revenue(valid_transactions)
    avg_transaction = total_revenue / len(valid_transactions) if valid_transactions else 0
    
    report_lines.append(f"Total Revenue: ${total_revenue:,.2f}")
    report_lines.append(f"Average Transaction Value: ${avg_transaction:,.2f}")
    report_lines.append(f"Number of Transactions: {len(valid_transactions)}")
    report_lines.append("")
    
    # ========================================================================
    # Section 2: Regional Analysis
    # ========================================================================
    report_lines.append("=" * 80)
    report_lines.append("2. REGIONAL SALES ANALYSIS")
    report_lines.append("=" * 80)
    
    region_sales = region_wise_sales(valid_transactions)
    
    for region, data in region_sales.items():
        report_lines.append(f"\n{region}:")
        report_lines.append(f"  Total Sales: ${data['total_sales']:,.2f}")
        report_lines.append(f"  Transactions: {data['transaction_count']}")
        report_lines.append(f"  Market Share: {data['percentage']}%")
    report_lines.append("")
    
    # ========================================================================
    # Section 3: Top Products
    # ========================================================================
    report_lines.append("=" * 80)
    report_lines.append("3. TOP 10 SELLING PRODUCTS (by quantity)")
    report_lines.append("=" * 80)
    
    top_products = top_selling_products(valid_transactions, n=10)
    
    for i, (product, quantity, revenue) in enumerate(top_products, 1):
        report_lines.append(f"\n{i}. {product}")
        report_lines.append(f"   Units Sold: {quantity}")
        report_lines.append(f"   Total Revenue: ${revenue:,.2f}")
        report_lines.append(f"   Average Price: ${revenue/quantity:,.2f}" if quantity > 0 else "   Average Price: $0.00")
    report_lines.append("")
    
    # ========================================================================
    # Section 4: Customer Insights
    # ========================================================================
    report_lines.append("=" * 80)
    report_lines.append("4. TOP 10 CUSTOMERS (by spending)")
    report_lines.append("=" * 80)
    
    customers = customer_analysis(valid_transactions)
    
    for i, (customer_id, data) in enumerate(list(customers.items())[:10], 1):
        report_lines.append(f"\n{i}. Customer {customer_id}")
        report_lines.append(f"   Total Spent: ${data['total_spent']:,.2f}")
        report_lines.append(f"   Number of Orders: {data['purchase_count']}")
        report_lines.append(f"   Average Order Value: ${data['avg_order_value']:,.2f}")
        report_lines.append(f"   Unique Products Purchased: {len(data['products_bought'])}")
        
        # Show first 5 products
        products_preview = data['products_bought'][:5]
        if len(data['products_bought']) > 5:
            products_str = ', '.join(products_preview) + f", ... (+{len(data['products_bought']) - 5} more)"
        else:
            products_str = ', '.join(products_preview)
        report_lines.append(f"   Products: {products_str}")
    report_lines.append("")
    
    # ========================================================================
    # Section 5: Daily Trends & Peak Sales
    # ========================================================================
    report_lines.append("=" * 80)
    report_lines.append("5. DAILY SALES TRENDS")
    report_lines.append("=" * 80)
    
    # Peak sales day
    peak_date, peak_revenue, peak_count = find_peak_sales_day(valid_transactions)
    report_lines.append(f"\nPeak Sales Day:")
    report_lines.append(f"  Date: {peak_date}")
    report_lines.append(f"  Revenue: ${peak_revenue:,.2f}")
    report_lines.append(f"  Transactions: {peak_count}")
    report_lines.append("")
    
    # Daily trend summary
    daily_trend = daily_sales_trend(valid_transactions)
    report_lines.append(f"Total Days with Sales: {len(daily_trend)}")
    report_lines.append("")
    
    # Top 5 revenue days
    report_lines.append("Top 5 Revenue Days:")
    sorted_days = sorted(daily_trend.items(), key=lambda x: x[1]['revenue'], reverse=True)
    for i, (date, data) in enumerate(sorted_days[:5], 1):
        report_lines.append(f"  {i}. {date}")
        report_lines.append(f"     Revenue: ${data['revenue']:,.2f}")
        report_lines.append(f"     Transactions: {data['transaction_count']}")
        report_lines.append(f"     Unique Customers: {data['unique_customers']}")
    report_lines.append("")
    
    # Show first 7 days chronologically
    report_lines.append("First 7 Days of Sales:")
    for i, (date, data) in enumerate(list(daily_trend.items())[:7], 1):
        report_lines.append(f"  {date}: ${data['revenue']:,.2f} ({data['transaction_count']} transactions)")
    report_lines.append("")
    
    # ========================================================================
    # Section 6: Low Performing Products
    # ========================================================================
    report_lines.append("=" * 80)
    report_lines.append("6. LOW PERFORMING PRODUCTS (< 10 units sold)")
    report_lines.append("=" * 80)
    
    low_performers = low_performing_products(valid_transactions, threshold=10)
    
    if low_performers:
        report_lines.append(f"\nFound {len(low_performers)} low-performing products:")
        report_lines.append("")
        for i, (product, quantity, revenue) in enumerate(low_performers, 1):
            report_lines.append(f"{i}. {product}")
            report_lines.append(f"   Units Sold: {quantity}")
            report_lines.append(f"   Total Revenue: ${revenue:,.2f}")
    else:
        report_lines.append("\nNo low-performing products found with current threshold.")
    report_lines.append("")
    
    # ========================================================================
    # Section 7: Summary Statistics
    # ========================================================================
    report_lines.append("=" * 80)
    report_lines.append("7. SUMMARY STATISTICS")
    report_lines.append("=" * 80)
    report_lines.append(f"\nTotal Customers: {len(customers)}")
    report_lines.append(f"Total Products: {len(set(t['ProductName'] for t in valid_transactions))}")
    report_lines.append(f"Total Regions: {len(region_sales)}")
    report_lines.append(f"Average Daily Revenue: ${total_revenue/len(daily_trend):,.2f}" if daily_trend else "Average Daily Revenue: $0.00")
    report_lines.append("")
    
    # Footer
    report_lines.append("=" * 80)
    report_lines.append("END OF REPORT")
    report_lines.append("=" * 80)
    
    # ========================================================================
    # Save report
    # ========================================================================
    report_content = '\n'.join(report_lines)
    
    # Create output directory if it doesn't exist
    os.makedirs('output', exist_ok=True)
    
    # Save to file
    output_file = 'output/comprehensive_analysis_report.txt'
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(report_content)
        print(f"✓ Comprehensive report saved to: {output_file}")
    except Exception as e:
        print(f"ERROR saving report: {e}")
        return None
    
    # Print to console
    print("\n" + "=" * 80)
    print("REPORT PREVIEW")
    print("=" * 80)
    print(report_content)
    print("\n" + "=" * 80)
    print(f"✓ Full report available at: {output_file}")
    print("=" * 80 + "\n")
    
    return report_content


def main():
    """Main function to run the report generation"""
    try:
        report = generate_comprehensive_report()
        
        if report:
            print("\n✓ Report generation completed successfully!")
        else:
            print("\n✗ Report generation failed.")
            
    except ImportError as e:
        print("\n" + "=" * 80)
        print("IMPORT ERROR")
        print("=" * 80)
        print(f"Error: {e}")
        print("\nPossible solutions:")
        print("1. Make sure utils/__init__.py exists")
        print("2. Verify all functions exist in utils/data_processor.py")
        print("3. Check that you're running from the project root directory")
        print("4. Try running: python -m generate_analysis_report")
        print("=" * 80 + "\n")
        
    except FileNotFoundError as e:
        print("\n" + "=" * 80)
        print("FILE NOT FOUND ERROR")
        print("=" * 80)
        print(f"Error: {e}")
        print("\nMake sure:")
        print("1. data/sales_data.txt exists")
        print("2. You're running from the project root directory")
        print("=" * 80 + "\n")
        
    except Exception as e:
        print("\n" + "=" * 80)
        print("UNEXPECTED ERROR")
        print("=" * 80)
        print(f"Error: {e}")
        print("\nPlease check:")
        print("1. All required functions are implemented")
        print("2. Data file is valid")
        print("3. All dependencies are installed")
        print("=" * 80 + "\n")


if __name__ == "__main__":
    main()