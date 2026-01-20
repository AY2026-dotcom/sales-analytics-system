"""
Standalone analysis - all functions in one file
"""

from datetime import datetime
import os

# ============================================================================
# DATA LOADING FUNCTIONS
# ============================================================================

def read_sales_data(filename):
    """Read sales data from file"""
    encodings = ['utf-8', 'latin-1', 'cp1252']
    raw_lines = []
    
    for encoding in encodings:
        try:
            with open(filename, 'r', encoding=encoding, errors='ignore') as file:
                all_lines = file.readlines()
                data_lines = all_lines[1:]  # Skip header
                
                for line in data_lines:
                    cleaned_line = line.strip()
                    if cleaned_line:
                        raw_lines.append(cleaned_line)
                
                return raw_lines
        except:
            continue
    return []


def parse_transactions(raw_lines):
    """Parse raw lines into transaction dictionaries"""
    transactions = []
    
    for line in raw_lines:
        fields = line.split('|')
        
        if len(fields) != 8:
            continue
        
        try:
            transaction = {
                'TransactionID': fields[0].strip(),
                'Date': fields[1].strip(),
                'ProductID': fields[2].strip(),
                'ProductName': fields[3].strip(),
                'Quantity': int(fields[4].strip().replace(',', '')),
                'UnitPrice': float(fields[5].strip().replace(',', '')),
                'CustomerID': fields[6].strip(),
                'Region': fields[7].strip()
            }
            transactions.append(transaction)
        except:
            continue
    
    return transactions


def validate_transactions(transactions):
    """Validate transactions"""
    valid = []
    
    for t in transactions:
        if (t.get('TransactionID', '').startswith('T') and
            t.get('Quantity', 0) > 0 and
            t.get('UnitPrice', 0) >= 0 and
            t.get('CustomerID', '') and
            t.get('Region', '')):
            valid.append(t)
    
    return valid


# ============================================================================
# TASK 2.1: SALES SUMMARY CALCULATOR
# ============================================================================

def calculate_total_revenue(transactions):
    """Calculate total revenue"""
    total = 0.0
    for t in transactions:
        total += t['Quantity'] * t['UnitPrice']
    return total


def region_wise_sales(transactions):
    """Analyze sales by region"""
    region_data = {}
    
    for t in transactions:
        region = t['Region']
        revenue = t['Quantity'] * t['UnitPrice']
        
        if region not in region_data:
            region_data[region] = {'total_sales': 0.0, 'transaction_count': 0}
        
        region_data[region]['total_sales'] += revenue
        region_data[region]['transaction_count'] += 1
    
    grand_total = sum(d['total_sales'] for d in region_data.values())
    
    for region in region_data:
        pct = (region_data[region]['total_sales'] / grand_total * 100) if grand_total > 0 else 0
        region_data[region]['percentage'] = round(pct, 2)
    
    return dict(sorted(region_data.items(), key=lambda x: x[1]['total_sales'], reverse=True))


def top_selling_products(transactions, n=5):
    """Find top n products by quantity"""
    product_data = {}
    
    for t in transactions:
        product = t['ProductName']
        qty = t['Quantity']
        revenue = t['Quantity'] * t['UnitPrice']
        
        if product not in product_data:
            product_data[product] = {'total_quantity': 0, 'total_revenue': 0.0}
        
        product_data[product]['total_quantity'] += qty
        product_data[product]['total_revenue'] += revenue
    
    product_list = [(p, d['total_quantity'], d['total_revenue']) for p, d in product_data.items()]
    product_list.sort(key=lambda x: x[1], reverse=True)
    
    return product_list[:n]


def customer_analysis(transactions):
    """Analyze customer purchase patterns"""
    customer_data = {}
    
    for t in transactions:
        cust = t['CustomerID']
        amount = t['Quantity'] * t['UnitPrice']
        product = t['ProductName']
        
        if cust not in customer_data:
            customer_data[cust] = {
                'total_spent': 0.0,
                'purchase_count': 0,
                'products_bought': set()
            }
        
        customer_data[cust]['total_spent'] += amount
        customer_data[cust]['purchase_count'] += 1
        customer_data[cust]['products_bought'].add(product)
    
    for cust in customer_data:
        total = customer_data[cust]['total_spent']
        count = customer_data[cust]['purchase_count']
        customer_data[cust]['avg_order_value'] = round(total / count, 2) if count > 0 else 0.0
        customer_data[cust]['products_bought'] = sorted(list(customer_data[cust]['products_bought']))
    
    return dict(sorted(customer_data.items(), key=lambda x: x[1]['total_spent'], reverse=True))


# ============================================================================
# TASK 2.2: DATE-BASED ANALYSIS
# ============================================================================

def daily_sales_trend(transactions):
    """Analyze daily sales trends"""
    daily_data = {}
    
    for t in transactions:
        date = t['Date']
        revenue = t['Quantity'] * t['UnitPrice']
        customer = t['CustomerID']
        
        if date not in daily_data:
            daily_data[date] = {
                'revenue': 0.0,
                'transaction_count': 0,
                'customers': set()
            }
        
        daily_data[date]['revenue'] += revenue
        daily_data[date]['transaction_count'] += 1
        daily_data[date]['customers'].add(customer)
    
    result = {}
    for date, data in daily_data.items():
        result[date] = {
            'revenue': round(data['revenue'], 2),
            'transaction_count': data['transaction_count'],
            'unique_customers': len(data['customers'])
        }
    
    return dict(sorted(result.items()))


def find_peak_sales_day(transactions):
    """Find day with highest revenue"""
    daily_trend = daily_sales_trend(transactions)
    
    if not daily_trend:
        return (None, 0.0, 0)
    
    peak_date = max(daily_trend.items(), key=lambda x: x[1]['revenue'])
    return (peak_date[0], peak_date[1]['revenue'], peak_date[1]['transaction_count'])


# ============================================================================
# TASK 2.3: PRODUCT PERFORMANCE
# ============================================================================

def low_performing_products(transactions, threshold=10):
    """Find products with low sales"""
    product_data = {}
    
    for t in transactions:
        product = t['ProductName']
        qty = t['Quantity']
        revenue = t['Quantity'] * t['UnitPrice']
        
        if product not in product_data:
            product_data[product] = {'total_quantity': 0, 'total_revenue': 0.0}
        
        product_data[product]['total_quantity'] += qty
        product_data[product]['total_revenue'] += revenue
    
    low_performers = [
        (p, d['total_quantity'], d['total_revenue'])
        for p, d in product_data.items()
        if d['total_quantity'] < threshold
    ]
    
    low_performers.sort(key=lambda x: x[1])
    return low_performers


# ============================================================================
# MAIN REPORT GENERATION
# ============================================================================

def generate_report():
    """Generate comprehensive report"""
    
    print("Loading data...")
    raw_lines = read_sales_data('data/sales_data.txt')
    transactions = parse_transactions(raw_lines)
    valid_transactions = validate_transactions(transactions)
    
    print(f"Loaded {len(valid_transactions)} valid transactions\n")
    
    # Generate report
    report = []
    report.append("=" * 80)
    report.append("COMPREHENSIVE SALES ANALYSIS REPORT")
    report.append("=" * 80)
    report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append(f"Valid Transactions: {len(valid_transactions)}")
    report.append("")
    
    # Revenue
    total_rev = calculate_total_revenue(valid_transactions)
    report.append("1. TOTAL REVENUE")
    report.append(f"   ${total_rev:,.2f}")
    report.append("")
    
    # Regions
    regions = region_wise_sales(valid_transactions)
    report.append("2. REGIONAL SALES")
    for region, data in regions.items():
        report.append(f"   {region}: ${data['total_sales']:,.2f} ({data['percentage']}%)")
    report.append("")
    
    # Top Products
    top_prods = top_selling_products(valid_transactions, n=5)
    report.append("3. TOP 5 PRODUCTS")
    for i, (prod, qty, rev) in enumerate(top_prods, 1):
        report.append(f"   {i}. {prod}: {qty} units, ${rev:,.2f}")
    report.append("")
    
    # Top Customers
    customers = customer_analysis(valid_transactions)
    report.append("4. TOP 5 CUSTOMERS")
    for i, (cust, data) in enumerate(list(customers.items())[:5], 1):
        report.append(f"   {i}. {cust}: ${data['total_spent']:,.2f}")
    report.append("")
    
    # Peak Day
    peak_date, peak_rev, peak_count = find_peak_sales_day(valid_transactions)
    report.append("5. PEAK SALES DAY")
    report.append(f"   {peak_date}: ${peak_rev:,.2f} ({peak_count} transactions)")
    report.append("")
    
    # Low Performers
    low_prods = low_performing_products(valid_transactions, threshold=10)
    report.append("6. LOW PERFORMING PRODUCTS (< 10 units)")
    for prod, qty, rev in low_prods:
        report.append(f"   {prod}: {qty} units, ${rev:,.2f}")
    report.append("")
    
    report.append("=" * 80)
    
    # Save and print
    report_text = '\n'.join(report)
    
    os.makedirs('output', exist_ok=True)
    with open('output/analysis_report.txt', 'w') as f:
        f.write(report_text)
    
    print(report_text)
    print("\n✓ Report saved to: output/analysis_report.txt")


if __name__ == "__main__":
    generate_report()
    