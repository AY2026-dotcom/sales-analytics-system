import pandas as pd
import numpy as np


def clean_numeric_column(series):
    """
    Clean numeric data - remove commas and convert to float
    Uses pandas string operations
    """
    cleaned = series.astype(str).str.replace(',', '')
    return pd.to_numeric(cleaned, errors='coerce')


def validate_and_clean(df):
    """
    Validate and clean sales data using pandas
    Returns: valid_df, invalid_df
    """
    print("Cleaning and validating data...")
    
    # Make a copy
    data = df.copy()
    
    # Clean numeric columns
    data['Quantity'] = clean_numeric_column(data['Quantity'])
    data['UnitPrice'] = clean_numeric_column(data['UnitPrice'])
    
    # Create validation tracking columns
    data['Valid'] = True
    data['Reason'] = ''
    
    # Rule 1: TransactionID must start with 'T'
    mask_id = ~data['TransactionID'].astype(str).str.startswith('T')
    data.loc[mask_id, 'Valid'] = False
    data.loc[mask_id, 'Reason'] = 'Invalid TransactionID format'
    
    # Rule 2: Quantity must be positive
    mask_qty = (data['Quantity'].isna()) | (data['Quantity'] <= 0)
    data.loc[mask_qty & data['Valid'], 'Valid'] = False
    data.loc[mask_qty & data['Valid'], 'Reason'] = 'Invalid quantity'
    
    # Rule 3: UnitPrice must be non-negative
    mask_price = (data['UnitPrice'].isna()) | (data['UnitPrice'] < 0)
    data.loc[mask_price & data['Valid'], 'Valid'] = False
    data.loc[mask_price & data['Valid'], 'Reason'] = 'Invalid price'
    
    # Rule 4: CustomerID must exist
    mask_cust = data['CustomerID'].astype(str).str.strip() == ''
    data.loc[mask_cust & data['Valid'], 'Valid'] = False
    data.loc[mask_cust & data['Valid'], 'Reason'] = 'Missing CustomerID'
    
    # Rule 5: Region must exist
    mask_region = data['Region'].astype(str).str.strip() == ''
    data.loc[mask_region & data['Valid'], 'Valid'] = False
    data.loc[mask_region & data['Valid'], 'Reason'] = 'Missing Region'
    
    # Split into valid and invalid
    valid_df = data[data['Valid']].copy()
    invalid_df = data[~data['Valid']].copy()
    
    # Calculate TotalPrice for valid records
    valid_df['TotalPrice'] = valid_df['Quantity'] * valid_df['UnitPrice']
    
    # Remove validation columns from valid data
    valid_df = valid_df.drop(['Valid', 'Reason'], axis=1)
    
    print(f"Valid transactions: {len(valid_df)}")
    print(f"Invalid transactions: {len(invalid_df)}\n")
    
    return valid_df, invalid_df


def analyze_sales(df):
    """
    Analyze sales data using pandas and numpy
    """
    print("Analyzing sales data...")
    
    if df.empty:
        print("No data to analyze")
        return {}
    
    # Basic revenue metrics
    total_revenue = df['TotalPrice'].sum()
    avg_transaction = df['TotalPrice'].mean()
    median_transaction = df['TotalPrice'].median()
    
    # Using numpy for statistics
    std_dev = np.std(df['TotalPrice'])
    min_trans = np.min(df['TotalPrice'])
    max_trans = np.max(df['TotalPrice'])
    total_units = np.sum(df['Quantity'])
    
    # Sales by region using pandas groupby
    region_sales = df.groupby('Region')['TotalPrice'].sum().to_dict()
    
    # Product analysis using pandas
    product_analysis = df.groupby('ProductName').agg({
        'TotalPrice': 'sum',
        'Quantity': 'sum'
    }).rename(columns={'TotalPrice': 'revenue', 'Quantity': 'units'})
    
    # Top 5 customers
    top_customers = df.groupby('CustomerID')['TotalPrice'].sum().nlargest(5)
    
    # Top 5 products
    top_products = product_analysis.nlargest(5, 'revenue')
    
    print(f"Total Revenue: ${total_revenue:,.2f}")
    print(f"Transactions Analyzed: {len(df)}\n")
    
    # Convert to list of tuples for reporting
    top_customers_list = [(cust, spend) for cust, spend in top_customers.items()]
    top_products_list = [(prod, {'revenue': row['revenue'], 'units': row['units']}) 
                         for prod, row in top_products.iterrows()]
    
    return {
        'total_revenue': total_revenue,
        'transaction_count': len(df),
        'avg_transaction': avg_transaction,
        'median_transaction': median_transaction,
        'std_dev': std_dev,
        'min_transaction': min_trans,
        'max_transaction': max_trans,
        'total_units': total_units,
        'region_sales': region_sales,
        'top_customers': top_customers_list,
        'top_products': top_products_list
    }