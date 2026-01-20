"""
Demo script showing Tasks 1.1, 1.2, and 1.3
"""

from utils.file_handler import read_sales_data, parse_transactions, validate_and_filter

def main():
    print("\n" + "=" * 75)
    print("SALES DATA PROCESSING DEMO")
    print("Demonstrating Tasks 1.1, 1.2, and 1.3")
    print("=" * 75)
    
    # TASK 1.1: Read Sales Data
    print("\n" + "=" * 75)
    print("TASK 1.1: Reading Sales Data with Encoding Handling")
    print("=" * 75)
    
    raw_lines = read_sales_data('data/sales_data.txt')
    
    if not raw_lines:
        print("Failed to read data. Exiting.")
        return
    
    print(f"✓ Successfully read {len(raw_lines)} lines")
    
    # TASK 1.2: Parse Transactions
    print("\n" + "=" * 75)
    print("TASK 1.2: Parsing and Cleaning Data")
    print("=" * 75)
    
    transactions = parse_transactions(raw_lines)
    
    print(f"✓ Successfully parsed {len(transactions)} transactions")
    
    # Show sample transaction
    if transactions:
        print(f"\nSample Transaction:")
        sample = transactions[0]
        for key, value in sample.items():
            print(f"  {key}: {value} ({type(value).__name__})")
    
    # TASK 1.3: Validate and Filter
    print("\n" + "=" * 75)
    print("TASK 1.3: Validation and Filtering")
    print("=" * 75)
    
    # Example 1: Just validate
    print("\n--- Example 1: Validation Only ---")
    valid, invalid_count, summary = validate_and_filter(transactions)
    
    # Example 2: Filter by region
    print("\n--- Example 2: Filter by Region ---")
    valid_north, _, summary_north = validate_and_filter(
        transactions,
        region='North'
    )
    
    # Example 3: Filter by amount
    print("\n--- Example 3: Filter by Amount Range ---")
    valid_amount, _, summary_amount = validate_and_filter(
        transactions,
        min_amount=5000,
        max_amount=20000
    )
    
    # Final Report
    print("\n" + "=" * 75)
    print("PROCESSING COMPLETE")
    print("=" * 75)
    print(f"Total records processed: {len(raw_lines)}")
    print(f"Successfully parsed: {len(transactions)}")
    print(f"Valid transactions: {len(valid)}")
    print(f"Invalid transactions: {invalid_count}")
    print("=" * 75)
    print("\n✓ All tasks completed successfully!\n")


if __name__ == "__main__":
    main()