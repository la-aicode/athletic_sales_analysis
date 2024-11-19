import pandas as pd

# Load the CSV files into DataFrames
data_2020 = pd.read_csv('athletic_sales_2020.csv')
data_2021 = pd.read_csv('athletic_sales_2021.csv')

# Combine the DataFrames using an inner join to include only matching columns
combined_data = pd.concat([data_2020, data_2021], join='inner', ignore_index=True)

# Reset the index
combined_data.reset_index(drop=True, inplace=True)

# Display the combined DataFrame
print(combined_data.head())


# Check for null values in the combined DataFrame
null_values = combined_data.isnull().sum()
print("Null Values:\n", null_values)

# Check each column's data type before conversion
data_types_before = combined_data.dtypes
print("\nData Types Before Conversion:\n", data_types_before)

# Convert the "invoice_date" column to a datetime data type
combined_data['invoice_date'] = pd.to_datetime(combined_data['invoice_date'], errors='coerce')

# Check the data type of the "invoice_date" column after conversion
data_types_after = combined_data.dtypes
print("\nData Types After Conversion:\n", data_types_after)

#-----------Determine which Region Sold the Most Products--------
# Group the data by "region", "state", and "city" to calculate total units sold
region_sales = combined_data.groupby(['region', 'state', 'city'], as_index=False).agg({'units_sold': 'sum'})

# Rename the aggregated column to reflect it represents total products sold
region_sales.rename(columns={'units_sold': 'total_units_sold'}, inplace=True)

# Sort the DataFrame in descending order based on total products sold
region_sales_sorted = region_sales.sort_values(by='total_units_sold', ascending=False)

# Extract the top five regions with their states and cities
top_5_regions = region_sales_sorted.head()

# Display the top five regions
print(top_5_regions)


#-----Determine which Retailer had the Most Sales----
# Group the data by "region", "state", and "city" to calculate total sales
region_sales = combined_data.groupby(['region', 'state', 'city']).agg({'total_sales': 'sum'})

# Rename the aggregated column to indicate it represents total sales
region_sales.rename(columns={'total_sales': 'total_sales_generated'}, inplace=True)

# Sort the results in descending order of total sales
region_sales_sorted = region_sales.sort_values(by='total_sales_generated', ascending=False)

# Extract the top five regions with their states and cities
top_5_regions_sales = region_sales_sorted.head()

# Display the results
print(top_5_regions_sales)

#--Using Pivot Table--
# Create a pivot table with total sales aggregated
region_sales_pivot = combined_data.pivot_table(
    values='total_sales',
    index=['region', 'state', 'city'],
    aggfunc='sum'
)

# Rename the column to indicate it represents total sales
region_sales_pivot.rename(columns={'total_sales': 'total_sales_generated'}, inplace=True)

# Sort the results in descending order of total sales
region_sales_pivot_sorted = region_sales_pivot.sort_values(by='total_sales_generated', ascending=False)

# Extract the top five regions
top_5_regions_sales_pivot = region_sales_pivot_sorted.head()

# Display the results
print(top_5_regions_sales_pivot)


#----Determine which Retailer Sold the Most Women's Athletic Footwear----
# Filter the combined DataFrame for rows where the product is "Women's Athletic Footwear"
womens_athletic_footwear_sales = combined_data[combined_data['product'] == "Women's Athletic Footwear"]

# Display the first few rows of the filtered DataFrame
print(womens_athletic_footwear_sales.head())

# Filter the combined DataFrame for Women's Athletic Footwear
womens_footwear_sales = combined_data[combined_data['product'] == "Women's Athletic Footwear"]

# Group the data by "retailer", "region", "state", and "city" and aggregate the total units sold
retailer_sales = womens_footwear_sales.groupby(['retailer', 'region', 'state', 'city']).agg({'units_sold': 'sum'})

# Rename the aggregated column to reflect total units sold
retailer_sales.rename(columns={'units_sold': 'total_units_sold'}, inplace=True)

# Sort the results in descending order by total units sold
retailer_sales_sorted = retailer_sales.sort_values(by='total_units_sold', ascending=False)

# Extract the top five retailers along with their regions, states, and cities
top_5_retailers = retailer_sales_sorted.head()

# Display the results
print(top_5_retailers)

# Filter the combined DataFrame for Women's Athletic Footwear
womens_footwear_sales = combined_data[combined_data['product'] == "Women's Athletic Footwear"]

# Create a pivot table with the desired columns and aggregate by total units sold
retailer_sales_pivot = womens_footwear_sales.pivot_table(
    values='units_sold',
    index=['retailer', 'region', 'state', 'city'],
    aggfunc='sum'
)

# Rename the aggregated column to reflect total units sold
retailer_sales_pivot.rename(columns={'units_sold': 'total_units_sold'}, inplace=True)

# Sort the results in descending order by total units sold
retailer_sales_pivot_sorted = retailer_sales_pivot.sort_values(by='total_units_sold', ascending=False)

# Extract the top five rows
top_5_retailers_pivot = retailer_sales_pivot_sorted.head()

# Display the results
print(top_5_retailers_pivot)


#----Determine the Day with the Most Women's Athletic Footwear Sales---
# Filter the combined DataFrame for Women's Athletic Footwear
womens_footwear_sales = combined_data[combined_data['product'] == "Women's Athletic Footwear"]

# Create a pivot table with "invoice_date" as the index and "total_sales" as the values
pivot_table = womens_footwear_sales.pivot_table(
    values='total_sales',
    index='invoice_date',
    aggfunc='sum'
)

# Rename the aggregated column to indicate it represents total sales
pivot_table.rename(columns={'total_sales': 'total_sales_per_day'}, inplace=True)

# Resample the pivot table into daily bins and calculate total sales for each day
daily_sales = pivot_table.resample('D').sum()

# Sort the resampled DataFrame in descending order to find the top 10 days
top_10_days = daily_sales.sort_values(by='total_sales_per_day', ascending=False).head(10)

# Display the top 10 days with the most women's athletic footwear sales
print(top_10_days)

#----Determine the Week with the Most Women's Athletic Footwear Sales---
# Resample the pivot table into weekly bins and calculate total sales for each week
weekly_sales = pivot_table.resample('W').sum()

# Sort the resampled DataFrame in descending order to find the top 10 weeks
top_10_weeks = weekly_sales.sort_values(by='total_sales_per_day', ascending=False).head(10)

# Display the top 10 weeks with the most women's athletic footwear sales
print(top_10_weeks)
