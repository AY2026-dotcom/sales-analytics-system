from utils.file_handler import read_sales_data

# Test Task 1.1
print("=" * 70)
print("TESTING TASK 1.1: Read Sales Data with Encoding Handling")
print("=" * 70)

raw_lines = read_sales_data('data/sales_data.txt')

print(f"\nNumber of lines read: {len(raw_lines)}")
print(f"\nFirst 3 lines:")
for i, line in enumerate(raw_lines[:3], 1):
    print(f"{i}. {line}")

print("\n✓ Task 1.1 Complete!")

# Test Task 1.2
print("\n" + "=" * 70)
print("TESTING TASK 1.2: Parse and Clean Data")
print("=" * 70)

transactions = parse_transactions(raw_lines)

print(f"Total parsed transactions: {len(transactions)}")
print(f"\nFirst transaction details:")
print(f"  Transaction ID: {transactions[0]['TransactionID']}")
print(f"  Product: {transactions[0]['ProductName']}")
print(f"  Quantity: {transactions[0]['Quantity']} (type: {type(transactions[0]['Quantity']).__name__})")
print(f"  Unit Price: {transactions[0]['UnitPrice']} (type: {type(transactions[0]['UnitPrice']).__name__})")
print(f"  Customer: {transactions[0]['CustomerID']}")
print(f"  Region: {transactions[0]['Region']}")

print("\n✓ Task 1.2 Complete!")

# Test Task 1.3
print("\n" + "=" * 70)
print("TESTING TASK 1.3: Data Validation and Filtering")
print("=" * 70)

# Test 1: Validation only (no filters)
print("\nTest 1: Validation only")
valid_trans, invalid_count, summary = validate_and_filter(transactions)

# Test 2: Filter by region
print("\n\nTest 2: Filter by Region = 'North'")
valid_trans, invalid_count, summary = validate_and_filter(
    transactions, 
    region='North'
)

# Test 3: Filter by amount range
print("\n\nTest 3: Filter by amount range (min=$5000, max=$50000)")
valid_trans, invalid_count, summary = validate_and_filter(
    transactions,
    min_amount=5000,
    max_amount=50000
)

# Test 4: Combined filters
print("\n\nTest 4: Combined filters (Region='East', min=$10000)")
valid_trans, invalid_count, summary = validate_and_filter(
    transactions,
    region='East',
    min_amount=10000
)

print("\n✓ Task 1.3 Complete!")
