# athletic_sales_analysis# Sales Data Analysis

This project analyzes sales data for athletic products across various retailers, regions, states, and cities. The dataset includes sales information for 2020 and 2021. Below is a summary of the operations performed and the corresponding code.

## Table of Contents

1. [Data Preparation](#data-preparation)
2. [Combining Data](#combining-data)
3. [Data Cleaning](#data-cleaning)
4. [Analysis](#analysis)
    - [Region with the Most Products Sold](#region-with-the-most-products-sold)
    - [Women's Athletic Footwear Sales](#womens-athletic-footwear-sales)
    - [Top Retailers for Women's Athletic Footwear](#top-retailers-for-womens-athletic-footwear)
    - [Daily Sales Analysis](#daily-sales-analysis)
    - [Weekly Sales Analysis](#weekly-sales-analysis)
5. [Requirements](#requirements)

---

## Data Preparation

### Load CSV Files
```python
import pandas as pd

# Load the two CSV files into DataFrames
data_2020 = pd.read_csv('athletic_sales_2020.csv')
data_2021 = pd.read_csv('athletic_sales_2021.csv')

Combining Data
Combine the Two DataFrames by Rows
# Combine the DataFrames by rows and reset the index
combined_data = pd.concat([data_2020, data_2021], ignore_index=True)

Data Cleaning
Check for Null Values and Data Types
# Check for null values
null_values = combined_data.isnull().sum()
print(null_values)

# Check data types
print(combined_data.dtypes)

Convert invoice_date to Datetime
# Convert the "invoice_date" column to datetime
combined_data['invoice_date'] = pd.to_datetime(combined_data['invoice_date'], errors='coerce')

Analysis
Region with the Most Products Sold
# Group by region, state, and city to calculate total units sold
region_sales = combined_data.groupby(['region', 'state', 'city']).agg({'units_sold': 'sum'})

# Rename the column and sort
region_sales.rename(columns={'units_sold': 'total_units_sold'}, inplace=True)
region_sales_sorted = region_sales.sort_values(by='total_units_sold', ascending=False)

# Display top 5 regions
top_5_regions = region_sales_sorted.head()
print(top_5_regions)

Women's Athletic Footwear Sales
Filter the Data
# Filter for Women's Athletic Footwear sales
womens_footwear_sales = combined_data[combined_data['product'] == "Women's Athletic Footwear"]

Top Retailers for Women's Athletic Footwear
# Group by retailer, region, state, and city to calculate total units sold
retailer_sales = womens_footwear_sales.groupby(['retailer', 'region', 'state', 'city']).agg({'units_sold': 'sum'})

# Rename the column and sort
retailer_sales.rename(columns={'units_sold': 'total_units_sold'}, inplace=True)
retailer_sales_sorted = retailer_sales.sort_values(by='total_units_sold', ascending=False)

# Display top 5 retailers
top_5_retailers = retailer_sales_sorted.head()
print(top_5_retailers)

Daily Sales Analysis
# Create a pivot table for daily sales
pivot_table = womens_footwear_sales.pivot_table(
    values='total_sales',
    index='invoice_date',
    aggfunc='sum'
)

# Resample into daily bins
daily_sales = pivot_table.resample('D').sum()

# Sort to find the top 10 days
top_10_days = daily_sales.sort_values(by='total_sales', ascending=False).head(10)
print(top_10_days)

Weekly Sales Analysis
# Resample into weekly bins
weekly_sales = pivot_table.resample('W').sum()

# Rename column and sort
weekly_sales.rename(columns={'total_sales': 'total_sales_per_week'}, inplace=True)
sorted_weekly_sales = weekly_sales.sort_values(by='total_sales_per_week', ascending=False)

# Display the top 10 weeks
print(sorted_weekly_sales)
