import pandas as pd
import urllib.request
import json


def categorize_product(product_name):
    """
    Categorize product based on name
    """
    name = str(product_name).lower()
    
    if 'laptop' in name:
        return 'Computers'
    elif 'mouse' in name or 'keyboard' in name:
        return 'Peripherals'
    elif 'monitor' in name or 'webcam' in name:
        return 'Display Devices'
    elif 'headphone' in name:
        return 'Audio Equipment'
    elif 'cable' in name or 'charger' in name:
        return 'Accessories'
    elif 'hard drive' in name:
        return 'Storage Devices'
    else:
        return 'Electronics'


def enrich_with_categories(df):
    """
    Add product categories using pandas apply
    """
    print("Adding product categories...")
    
    # Use pandas apply - applies function to each row
    df['Category'] = df['ProductName'].apply(categorize_product)
    
    print(f"Categories added to {len(df)} products\n")
    return df


def fetch_exchange_rates():
    """
    Fetch current exchange rates from API
    """
    print("Fetching exchange rates...")
    
    try:
        url = "https://api.exchangerate-api.com/v4/latest/USD"
        
        with urllib.request.urlopen(url, timeout=10) as response:
            data = json.loads(response.read().decode())
            
            rates = {
                'EUR': data['rates'].get('EUR'),
                'GBP': data['rates'].get('GBP'),
                'INR': data['rates'].get('INR'),
                'date': data.get('date')
            }
            print("Exchange rates fetched successfully\n")
            return rates
    
    except urllib.error.URLError:
        print("Could not connect to API - using default rates\n")
        return {'EUR': 0.92, 'GBP': 0.79, 'INR': 83.12, 'date': '2024-12-01'}
    except Exception as e:
        print(f"API error: {e} - using default rates\n")
        return {'EUR': 0.92, 'GBP': 0.79, 'INR': 83.12, 'date': '2024-12-01'}