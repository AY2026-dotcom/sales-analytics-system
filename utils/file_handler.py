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