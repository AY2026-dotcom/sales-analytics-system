def read_sales_data(filename):
    """
    Reads sales data from file handling encoding issues
    Returns: list of raw lines (strings)
    
    Expected Output Format:
    ['T001|2024-12-01|P101|Laptop|2|45000|C001|North', ...]
    
    Requirements:
    - Use 'with' statement
    - Handle different encodings (try 'utf-8', 'latin-1', 'cp1252')
    - Handle FileNotFoundError with appropriate error message
    - Skip the header row
    - Remove empty lines
    """
    
    # List of encodings to try
    encodings = ['utf-8', 'latin-1', 'cp1252']
    raw_lines = []
    
    # Try each encoding until one works
    for encoding in encodings:
        try:
            print(f"Attempting to read file with {encoding} encoding...")
            
            with open(filename, 'r', encoding=encoding, errors='ignore') as file:
                # Read all lines from file
                all_lines = file.readlines()
                
                # Skip the header (first line)
                data_lines = all_lines[1:]
                
                # Process each line
                for line in data_lines:
                    # Remove leading/trailing whitespace and newlines
                    cleaned_line = line.strip()
                    
                    # Skip empty lines
                    if cleaned_line:
                        raw_lines.append(cleaned_line)
                
                print(f"Successfully read file using {encoding} encoding")
                print(f"Total lines read: {len(raw_lines)}\n")
                
                # If we got here, reading was successful
                return raw_lines
        
        except FileNotFoundError:
            # File doesn't exist - print error and stop trying
            print(f"ERROR: File '{filename}' not found!")
            print(f"Please make sure the file exists in the correct location.")
            return []
        
        except Exception as e:
            # This encoding didn't work, try next one
            print(f"Failed with {encoding}: {e}")
            continue
    
    # If all encodings failed
    print("ERROR: Could not read file with any encoding")
    return []


import pandas as pd

def read_sales_data(file_path):
    """
    Read sales data file using pandas
    """
    try:
        print(f"Reading file: {file_path}")
        
        # Read pipe-delimited file
        df = pd.read_csv(
            file_path,
            sep='|',
            encoding='utf-8',
            on_bad_lines='skip'
        )
        
        print(f"Columns found: {list(df.columns)}")
        print(f"Total records read: {len(df)}\n")
        
        return df
    
    except FileNotFoundError:
        print(f"ERROR: File '{file_path}' not found")
        return pd.DataFrame()
    except Exception as e:
        print(f"ERROR reading file: {e}")
        return pd.DataFrame()


def write_report(file_path, content):
    """
    Write text report to file
    """
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Saved: {file_path}")
        return True
    except Exception as e:
        print(f"ERROR writing report: {e}")
        return False


def save_cleaned_data(file_path, df):
    """
    Save DataFrame to pipe-delimited file
    """
    try:
        df.to_csv(file_path, sep='|', index=False, encoding='utf-8')
        print(f"Saved: {file_path}")
        return True
    except Exception as e:
        print(f"ERROR saving data: {e}")
        return False


def parse_transactions(raw_lines):
    """
    Parses raw lines into clean list of dictionaries
    
    Returns: list of dictionaries with keys:
    ['TransactionID', 'Date', 'ProductID', 'ProductName',
     'Quantity', 'UnitPrice', 'CustomerID', 'Region']
    
    Expected Output Format:
    [
        {
            'TransactionID': 'T001',
            'Date': '2024-12-01',
            'ProductID': 'P101',
            'ProductName': 'Laptop',
            'Quantity': 2,           # int type
            'UnitPrice': 45000.0,    # float type
            'CustomerID': 'C001',
            'Region': 'North'
        },
        ...
    ]
    
    Requirements:
    - Split by pipe delimiter '|'
    - Handle commas within ProductName (remove or replace)
    - Remove commas from numeric fields and convert to proper types
    - Convert Quantity to int
    - Convert UnitPrice to float
    - Skip rows with incorrect number of fields
    """
    
    transactions = []
    skipped_count = 0
    
    # Define expected column headers
    headers = ['TransactionID', 'Date', 'ProductID', 'ProductName', 
               'Quantity', 'UnitPrice', 'CustomerID', 'Region']
    
    print("Parsing transactions...")
    
    for line_num, line in enumerate(raw_lines, 1):
        # Split by pipe delimiter
        fields = line.split('|')
        
        # Check if we have the correct number of fields (8 fields expected)
        if len(fields) != 8:
            print(f"  Skipping line {line_num}: Incorrect number of fields (expected 8, got {len(fields)})")
            skipped_count += 1
            continue
        
        try:
            # Extract fields
            transaction_id = fields[0].strip()
            date = fields[1].strip()
            product_id = fields[2].strip()
            product_name = fields[3].strip()
            quantity_str = fields[4].strip()
            unit_price_str = fields[5].strip()
            customer_id = fields[6].strip()
            region = fields[7].strip()
            
            # Handle commas in ProductName
            # Replace commas with spaces or keep them (business decision)
            # Here we'll keep the comma but you could replace with: product_name.replace(',', ' ')
            product_name_clean = product_name
            
            # Remove commas from Quantity and convert to int
            quantity_clean = quantity_str.replace(',', '')
            quantity = int(quantity_clean)
            
            # Remove commas from UnitPrice and convert to float
            unit_price_clean = unit_price_str.replace(',', '')
            unit_price = float(unit_price_clean)
            
            # Create transaction dictionary
            transaction = {
                'TransactionID': transaction_id,
                'Date': date,
                'ProductID': product_id,
                'ProductName': product_name_clean,
                'Quantity': quantity,
                'UnitPrice': unit_price,
                'CustomerID': customer_id,
                'Region': region
            }
            
            transactions.append(transaction)
        
        except ValueError as e:
            # Conversion to int or float failed
            print(f"  Skipping line {line_num}: Data conversion error - {e}")
            skipped_count += 1
            continue
        
        except Exception as e:
            # Any other error
            print(f"  Skipping line {line_num}: Unexpected error - {e}")
            skipped_count += 1
            continue
    
    print(f"\nParsing complete:")
    print(f"  Successfully parsed: {len(transactions)} transactions")
    print(f"  Skipped: {skipped_count} lines\n")
    
    return transactions


def validate_and_filter(transactions, region=None, min_amount=None, max_amount=None):
    """
    Validates transactions and applies optional filters
    
    Parameters:
    - transactions: list of transaction dictionaries
    - region: filter by specific region (optional)
    - min_amount: minimum transaction amount (Quantity * UnitPrice) (optional)
    - max_amount: maximum transaction amount (optional)
    
    Returns: tuple (valid_transactions, invalid_count, filter_summary)
    
    Expected Output Format:
    (
        [list of valid filtered transactions],
        5,  # count of invalid transactions
        {
            'total_input': 100,
            'invalid': 5,
            'filtered_by_region': 20,
            'filtered_by_amount': 10,
            'final_count': 65
        }
    )
    
    Validation Rules:
    - Quantity must be > 0
    - UnitPrice must be > 0
    - All required fields must be present
    - TransactionID must start with 'T'
    - ProductID must start with 'P'
    - CustomerID must start with 'C'
    
    Filter Display:
    - Print available regions to user before filtering
    - Print transaction amount range (min/max) to user
    - Show count of records after each filter applied
    """
    
    print("\n" + "=" * 70)
    print("VALIDATION AND FILTERING")
    print("=" * 70)
    
    # Track counts
    total_input = len(transactions)
    invalid_count = 0
    filtered_by_region_count = 0
    filtered_by_amount_count = 0
    
    # Step 1: VALIDATION
    print("\nStep 1: Validating transactions...")
    valid_transactions = []
    invalid_transactions = []
    
    for transaction in transactions:
        is_valid = True
        reasons = []
        
        # Validate Quantity > 0
        if transaction.get('Quantity', 0) <= 0:
            is_valid = False
            reasons.append("Quantity must be > 0")
        
        # Validate UnitPrice > 0
        if transaction.get('UnitPrice', 0) <= 0:
            is_valid = False
            reasons.append("UnitPrice must be > 0")
        
        # Validate all required fields are present
        required_fields = ['TransactionID', 'Date', 'ProductID', 'ProductName', 
                          'Quantity', 'UnitPrice', 'CustomerID', 'Region']
        for field in required_fields:
            if not transaction.get(field):
                is_valid = False
                reasons.append(f"Missing {field}")
        
        # Validate TransactionID starts with 'T'
        if not str(transaction.get('TransactionID', '')).startswith('T'):
            is_valid = False
            reasons.append("TransactionID must start with 'T'")
        
        # Validate ProductID starts with 'P'
        if not str(transaction.get('ProductID', '')).startswith('P'):
            is_valid = False
            reasons.append("ProductID must start with 'P'")
        
        # Validate CustomerID starts with 'C'
        if not str(transaction.get('CustomerID', '')).startswith('C'):
            is_valid = False
            reasons.append("CustomerID must start with 'C'")
        
        if is_valid:
            valid_transactions.append(transaction)
        else:
            invalid_count += 1
            invalid_transactions.append({
                'transaction': transaction,
                'reasons': reasons
            })
            print(f"  Invalid: {transaction.get('TransactionID', 'Unknown')} - {', '.join(reasons)}")
    
    print(f"\nValidation Results:")
    print(f"  Valid: {len(valid_transactions)}")
    print(f"  Invalid: {invalid_count}")
    
    # Step 2: DISPLAY AVAILABLE OPTIONS
    print("\n" + "-" * 70)
    print("Step 2: Available Filter Options")
    print("-" * 70)
    
    # Get unique regions
    regions = set()
    for t in valid_transactions:
        regions.add(t['Region'])
    
    print(f"\nAvailable Regions: {', '.join(sorted(regions))}")
    
    # Calculate transaction amounts and find min/max
    amounts = []
    for t in valid_transactions:
        amount = t['Quantity'] * t['UnitPrice']
        amounts.append(amount)
    
    if amounts:
        min_trans_amount = min(amounts)
        max_trans_amount = max(amounts)
        print(f"Transaction Amount Range: ${min_trans_amount:,.2f} - ${max_trans_amount:,.2f}")
    
    # Step 3: APPLY FILTERS
    filtered_transactions = valid_transactions.copy()
    
    # Apply region filter
    if region:
        print(f"\n" + "-" * 70)
        print(f"Step 3a: Filtering by Region = '{region}'")
        print("-" * 70)
        
        before_count = len(filtered_transactions)
        filtered_transactions = [t for t in filtered_transactions if t['Region'] == region]
        after_count = len(filtered_transactions)
        filtered_by_region_count = before_count - after_count
        
        print(f"  Records before filter: {before_count}")
        print(f"  Records after filter: {after_count}")
        print(f"  Records filtered out: {filtered_by_region_count}")
    
    # Apply amount filter
    if min_amount is not None or max_amount is not None:
        print(f"\n" + "-" * 70)
        print(f"Step 3b: Filtering by Amount")
        print("-" * 70)
        
        if min_amount is not None:
            print(f"  Minimum amount: ${min_amount:,.2f}")
        if max_amount is not None:
            print(f"  Maximum amount: ${max_amount:,.2f}")
        
        before_count = len(filtered_transactions)
        
        temp_filtered = []
        for t in filtered_transactions:
            amount = t['Quantity'] * t['UnitPrice']
            
            # Check min_amount
            if min_amount is not None and amount < min_amount:
                continue
            
            # Check max_amount
            if max_amount is not None and amount > max_amount:
                continue
            
            temp_filtered.append(t)
        
        filtered_transactions = temp_filtered
        after_count = len(filtered_transactions)
        filtered_by_amount_count = before_count - after_count
        
        print(f"  Records before filter: {before_count}")
        print(f"  Records after filter: {after_count}")
        print(f"  Records filtered out: {filtered_by_amount_count}")
    
    # Create summary
    filter_summary = {
        'total_input': total_input,
        'invalid': invalid_count,
        'filtered_by_region': filtered_by_region_count,
        'filtered_by_amount': filtered_by_amount_count,
        'final_count': len(filtered_transactions)
    }
    
    # Final summary
    print("\n" + "=" * 70)
    print("FINAL SUMMARY")
    print("=" * 70)
    print(f"  Total input transactions: {filter_summary['total_input']}")
    print(f"  Invalid transactions: {filter_summary['invalid']}")
    print(f"  Filtered by region: {filter_summary['filtered_by_region']}")
    print(f"  Filtered by amount: {filter_summary['filtered_by_amount']}")
    print(f"  Final valid transactions: {filter_summary['final_count']}")
    print("=" * 70 + "\n")
    
    return filtered_transactions, invalid_count, filter_summary

