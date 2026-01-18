# sales-analytics-system
Module 3: Python Programming Assignment
# Sales Data Analytics System

A comprehensive Python-based sales analytics system leveraging **Pandas** and **NumPy** for efficient data processing, validation, and statistical analysis.

## Author
Akanksha Yadav  
Python Data Analytics Assignment

## Overview

This system processes messy sales transaction data, performs data quality validation, integrates with external APIs, conducts statistical analysis, and generates comprehensive business reports.

## Technologies Used

- **Python 3.x** - Core programming language
- **Pandas** - Data manipulation and analysis
- **NumPy** - Numerical computations and statistics
- **urllib** - HTTP library for API integration
- **json** - JSON data parsing

## Key Features

✅ **Data Processing with Pandas**
- Efficient CSV/pipe-delimited file reading
- DataFrame-based data manipulation
- Vectorized operations for performance

✅ **Statistical Analysis with NumPy**
- Mean, median, standard deviation calculations
- Min/max value analysis
- Numerical aggregations

✅ **Data Validation**
- Transaction ID format verification
- Quantity and price validation
- Missing field detection
- Automated data quality reporting

✅ **API Integration**
- Real-time exchange rate fetching
- Product categorization
- Error handling and fallback mechanisms

✅ **Comprehensive Reporting**
- Sales summary with statistics
- Invalid records tracking
- Multi-format output (TXT, CSV)

## Project Structure
```
sales-analytics-system/
├── README.md                          # Project documentation
├── main.py                            # Main program orchestrator
├── requirements.txt                   # Python dependencies
├── utils/                             # Utility modules
│   ├── __init__.py                    # Package initializer
│   ├── file_handler.py                # File I/O operations with Pandas
│   ├── data_processor.py              # Data cleaning and analysis
│   └── api_handler.py                 # API integration functions
├── data/                              # Input data directory
│   └── sales_data.txt                 # Sales transaction data (pipe-delimited)
└── output/                            # Generated reports (auto-created)
    ├── sales_summary_report.txt       # Main analysis report
    ├── invalid_records_report.txt     # Data quality report
    ├── cleaned_sales_data.txt         # Cleaned data (pipe-delimited)
    └── cleaned_sales_data.csv         # Cleaned data (CSV format)
```

## Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)
- Internet connection (for API calls)

### Setup Steps

1. **Clone the repository**
```bash
git clone https://github.com/YOUR-USERNAME/sales-analytics-system.git
cd sales-analytics-system
```

2. **Install required libraries**
```bash
python -m pip install pandas numpy
```

Or use requirements.txt:
```bash
python -m pip install -r requirements.txt
```

3. **Verify installation**
```bash
python -c "import pandas; import numpy; print('Ready to go!')"
```

## Usage

### Running the Program

Execute the main program:
```bash
python main.py
```

### Expected Output

The program will:
1. Read the sales data file
2. Display validation progress
3. Show analysis statistics in terminal
4. Generate 4 report files in the `output/` directory

### Console Output Example
```
===========================================================================
SALES DATA ANALYTICS SYSTEM
Powered by Pandas and NumPy
===========================================================================

STEP 1: Reading Sales Data
...
Valid transactions: 67
Invalid transactions: 10
...
Total Revenue: $1,234,567.89

PROCESSING COMPLETE!
===========================================================================
```

## Data Validation Rules

The system validates transactions based on these criteria:

| Rule | Validation Check |
|------|------------------|
| Transaction ID | Must start with 'T' |
| Quantity | Must be positive (> 0) |
| Unit Price | Must be non-negative (≥ 0) |
| Customer ID | Must be present |
| Region | Must be present |

Invalid records are logged with rejection reasons in `invalid_records_report.txt`.

## Output Reports

### 1. sales_summary_report.txt

Comprehensive analysis including:
- **Data Quality Metrics**: Valid vs invalid transaction counts
- **Revenue Analysis**: Total, average, median, std deviation
- **Statistical Insights**: Min/max transaction values, total units sold
- **Currency Conversions**: USD, EUR, GBP, INR
- **Regional Performance**: Sales breakdown with percentages
- **Top 5 Products**: By revenue and units sold
- **Top 5 Customers**: By total spending

### 2. invalid_records_report.txt

Details of rejected records:
- Transaction ID
- Rejection reason
- Product and customer information
- Helps identify data quality issues

### 3. cleaned_sales_data.txt

Pipe-delimited file with:
- All valid transactions
- Cleaned numeric fields
- Calculated total prices
- Added product categories

### 4. cleaned_sales_data.csv

Same as above in CSV format for easy viewing in Excel or other tools.

## Data Processing Pipeline
```
Raw Data (sales_data.txt)
    ↓
[Pandas Read CSV] - Read pipe-delimited file
    ↓
[Data Cleaning] - Remove commas, handle encoding
    ↓
[Validation] - Apply business rules
    ↓
[Split] - Valid vs Invalid records
    ↓
[Enrichment] - Add categories via API
    ↓
[Analysis] - Pandas groupby + NumPy stats
    ↓
[Reporting] - Generate multiple output formats
```

## Why Pandas and NumPy?

### Pandas Benefits
- **Performance**: Vectorized operations are 10-100x faster than loops
- **Simplicity**: Complex operations in single lines of code
- **Flexibility**: Easy data manipulation and transformation
- **Integration**: Works seamlessly with NumPy

### NumPy Benefits
- **Speed**: Optimized C libraries for numerical operations
- **Memory Efficiency**: Array operations use less memory
- **Mathematical Functions**: Extensive library of statistical functions
- **Industry Standard**: Used in data science and machine learning

### Code Comparison

**Without Pandas/NumPy:**
```python
total = 0
for transaction in transactions:
    total += transaction['price'] * transaction['quantity']
avg = total / len(transactions)
```

**With Pandas:**
```python
df['TotalPrice'] = df['Quantity'] * df['UnitPrice']
avg = df['TotalPrice'].mean()
```

## Dataset Information

- **Format**: Pipe-delimited (|)
- **Records**: ~77 transactions
- **Date Range**: December 2024
- **Regions**: North, South, East, West
- **Products**: 10 different product types

### Data Quality Issues Handled
✅ Comma-formatted numbers (e.g., "1,200")  
✅ Missing customer IDs  
✅ Missing regions  
✅ Zero or negative quantities  
✅ Negative prices  
✅ Invalid transaction ID formats  

## Error Handling

The system includes robust error handling for:
- File not found errors
- API connection failures
- Data parsing issues
- Invalid data formats
- Encoding problems
