"""
Comprehensive test for Tasks 1.1, 1.2, and 1.3
"""

from utils.file_handler import read_sales_data, parse_transactions, validate_and_filter

def test_task_1_1():
    """Test Task 1.1"""
    print("\n" + "="*70)
    print("TEST: Task 1.1 - Read Sales Data")
    print("="*70)
    
    raw_lines = read_sales_data('data/sales_data.txt')
    
    # Verify results
    assert len(raw_lines) > 0, "Should read at least some lines"
    assert len(raw_lines) >= 50 and len(raw_lines) <= 100, f"Should read 50-100 lines, got {len(raw_lines)}"
    assert all('|' in line for line in raw_lines), "All lines should be pipe-delimited"
    
    print("✓ Task 1.1 PASSED")
    return raw_lines


def test_task_1_2(raw_lines):
    """Test Task 1.2"""
    print("\n" + "="*70)
    print("TEST: Task 1.2 - Parse Transactions")
    print("="*70)
    
    transactions = parse_transactions(raw_lines)
    
    # Verify results
    assert len(transactions) > 0, "Should parse at least some transactions"
    
    # Check first transaction structure
    first = transactions[0]
    assert 'TransactionID' in first, "Should have TransactionID"
    assert 'Quantity' in first, "Should have Quantity"
    assert 'UnitPrice' in first, "Should have UnitPrice"
    
    # Check data types
    assert isinstance(first['Quantity'], int), f"Quantity should be int, got {type(first['Quantity'])}"
    assert isinstance(first['UnitPrice'], float), f"UnitPrice should be float, got {type(first['UnitPrice'])}"
    
    print("✓ Task 1.2 PASSED")
    return transactions


def test_task_1_3(transactions):
    """Test Task 1.3"""
    print("\n" + "="*70)
    print("TEST: Task 1.3 - Validate and Filter")
    print("="*70)
    
    # Test validation
    valid, invalid_count, summary = validate_and_filter(transactions)
    
    # Verify results
    assert 'total_input' in summary, "Summary should have total_input"
    assert 'invalid' in summary, "Summary should have invalid count"
    assert 'final_count' in summary, "Summary should have final_count"
    assert summary['total_input'] == len(transactions), "Total input should match input length"
    
    # Test region filter
    valid_north, _, summary_north = validate_and_filter(transactions, region='North')
    assert len(valid_north) < len(valid), "Filtered results should be smaller"
    
    # Test amount filter
    valid_amount, _, summary_amount = validate_and_filter(transactions, min_amount=10000)
    assert len(valid_amount) < len(valid), "Filtered results should be smaller"
    
    print("✓ Task 1.3 PASSED")
    return valid, invalid_count, summary


def main():
    print("\n" + "="*70)
    print("COMPREHENSIVE TASK TESTING")
    print("="*70)
    
    try:
        # Test each task
        raw_lines = test_task_1_1()
        transactions = test_task_1_2(raw_lines)
        valid, invalid_count, summary = test_task_1_3(transactions)
        
        # Final summary
        print("\n" + "="*70)
        print("ALL TESTS PASSED!")
        print("="*70)
        print(f"Lines read: {len(raw_lines)}")
        print(f"Transactions parsed: {len(transactions)}")
        print(f"Valid transactions: {len(valid)}")
        print(f"Invalid transactions: {invalid_count}")
        print("="*70)
        print("\n✓ All tasks implemented correctly!\n")
        
    except AssertionError as e:
        print(f"\n✗ TEST FAILED: {e}\n")
    except Exception as e:
        print(f"\n✗ ERROR: {e}\n")


if __name__ == "__main__":
    main()