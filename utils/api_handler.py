import requests

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
    

# =========================
# TASK 3.1 – API FUNCTIONS
# =========================

def fetch_all_products():
    url = "https://dummyjson.com/products?limit=100"
    products = []

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        for item in data.get("products", []):
            products.append({
                "id": item.get("id"),
                "title": item.get("title"),
                "category": item.get("category"),
                "brand": item.get("brand"),
                "price": item.get("price"),
                "rating": item.get("rating")
            })

        print(f"API SUCCESS: {len(products)} products fetched")

    except Exception as e:
        print("API ERROR: Unable to fetch products:", e)
        return []

    return products


def create_product_mapping(api_products):
    mapping = {}

    for product in api_products:
        mapping[product["id"]] = {
            "title": product["title"],
            "category": product["category"],
            "brand": product["brand"],
            "rating": product["rating"]
        }

    print("API SUCCESS: Product mapping created")
    return mapping

# =========================
# TASK 3.2 – DATA ENRICHMENT
# =========================

def enrich_sales_data(transactions, product_mapping):
    enriched = []

    for txn in transactions:
        new_txn = txn.copy()

        try:
            product_num = int(txn["ProductID"].replace("P", ""))

            if product_num in product_mapping:
                api_data = product_mapping[product_num]
                new_txn["API_Category"] = api_data["category"]
                new_txn["API_Brand"] = api_data["brand"]
                new_txn["API_Rating"] = api_data["rating"]
                new_txn["API_Match"] = True
            else:
                new_txn["API_Category"] = None
                new_txn["API_Brand"] = None
                new_txn["API_Rating"] = None
                new_txn["API_Match"] = False

        except Exception:
            new_txn["API_Category"] = None
            new_txn["API_Brand"] = None
            new_txn["API_Rating"] = None
            new_txn["API_Match"] = False

        enriched.append(new_txn)

    save_enriched_data(enriched)
    return enriched


def save_enriched_data(enriched_transactions, filename="data/enriched_sales_data.txt"):
    header = [
        "TransactionID", "Date", "ProductID", "ProductName",
        "Quantity", "UnitPrice", "CustomerID", "Region",
        "API_Category", "API_Brand", "API_Rating", "API_Match"
    ]

    with open(filename, "w", encoding="utf-8") as file:
        file.write("|".join(header) + "\n")

        for txn in enriched_transactions:
            row = [
                str(txn.get("TransactionID")),
                str(txn.get("Date")),
                str(txn.get("ProductID")),
                str(txn.get("ProductName")),
                str(txn.get("Quantity")),
                str(txn.get("UnitPrice")),
                str(txn.get("CustomerID")),
                str(txn.get("Region")),
                str(txn.get("API_Category") or ""),
                str(txn.get("API_Brand") or ""),
                str(txn.get("API_Rating") or ""),
                str(txn.get("API_Match"))
            ]
            file.write("|".join(row) + "\n")

    print(f"File saved: {filename}")

