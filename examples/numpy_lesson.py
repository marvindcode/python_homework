import pandas as pd

data = [1, 3, 5, 7, 9]
s = pd.Series(data, name="numbers")
print(s)

data1 = pd.Series([10, 20, 30], index=["a", "b", "c"])
print(data1)

data2 = pd.Series(['Tom', 'Li', 'Antonio', 'Mary'], index=[5, 2, 2, 3])
print(data2)

print(data2[2])

# print(data2[1])

data3 = data2.reset_index()
print(data3)

my_list = [10, 20, 30]
print(my_list[1])

# Series Example
my_series = pd.Series([10, 20, 30], index=["a", "b", "c"])
print(my_series["b"])  # Access by index label
# Output: 20

print(my_series.iloc[2]) # Access by integer position
# Output: 30

my_revised_series = my_series * 2
print(my_revised_series)


# Creating a DataFrame from a dict
data = {
    'Name': ['Alice', 'Bob', 'Charlie'],
    'Age': [24, 27, 22],
    'City': ['New York', 'San Francisco', 'Chicago']
}
df = pd.DataFrame(data)
print(df)

data_alice = {'Name': 'Alice', 'Age': 24, 'City': 'New York'}
data_bob = {'Name': 'Bob', 'Age': 27, 'City': 'San Francisco'}
data_charlie = {'Name': 'Charlie', 'Age': 22, 'City': 'Chicago'}
df = pd.DataFrame([data_alice, data_bob, data_charlie])
print(df)

import numpy as np # load the numpy library
# Create a Pandas DataFrame using NumPy arrays
data = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
df = pd.DataFrame(data, columns=['A', 'B', 'C'])

print(df)


data = pd.DataFrame({
    'Name': ['Alice', 'Bob', 'Charlie'],
    'Age': [24, 27, 22],
    'City': ['New York', 'San Francisco', 'Chicago']
})

more_data = pd.DataFrame({
  'Name': ['Fred', 'Barney'],
  'Age': [57, 55],
  'City': ['Bedrock', 'Bedrock']
})

combined_df = pd.concat([data, more_data], ignore_index=True)



import pandas as pd

data = {
    "Name": ["Alice", "Bob", "Charlie"],
    "Height": ["5.5", "unknown", "5.9"],  # "unknown" is not numeric
    "Weight": ["60", "70", "NaN"]        # "NaN" is a missing placeholder
}
df = pd.DataFrame(data)

print("Before conversion:")
print(df)

# Replace placeholders with NaN and convert to numeric
df["Height"] = df["Height"].replace("unknown", pd.NA)
df["Height"] = pd.to_numeric(df["Height"], errors="coerce")
df["Weight"] = pd.to_numeric(df["Weight"], errors="coerce")

print("\nAfter conversion to numeric:")
print(df)



data = {
    "Person": ["Alice", "Bob", "Charlie", "Dana", "Eve"],
    "Score": [10, np.nan, 20, None, 25],
    "City": ["New York", "Chicago", None, "Boston", "NaN"]
}
df = pd.DataFrame(data)

print("Original DataFrame:")
print(df)

# Strategy 1: Fill numeric missing values with a fixed number
df["Score_filled_fixed"] = df["Score"].fillna(0)

# Strategy 2: Fill numeric missing values with the column mean
mean_score = df["Score"].mean()  # ignoring NaNs
df["Score_filled_mean"] = df["Score"].fillna(mean_score)

# Strategy 3: Fill textual missing values with "Unknown"
df["City_filled"] = df["City"].replace("NaN", pd.NA).fillna("Unknown")

print("\nDataFrame after fillna strategies:")
print(df)



data = {
    "Day": ["Mon", "Tue", "Wed", "Thu", "Fri"],
    "Sales": [100, np.nan, 150, np.nan, 200]
}
df = pd.DataFrame(data)

print("Original Sales Data:")
print(df)

# Forward fill (propagate last valid observation forward)
df_ffill = df.copy()
df_ffill["Sales"] = df_ffill["Sales"].fillna(method="ffill")

# Backward fill (use next valid observation to fill gaps)
df_bfill = df.copy()
df_bfill["Sales"] = df_bfill["Sales"].fillna(method="bfill")

print("\nForward Fill Result:")
print(df_ffill)

print("\nBackward Fill Result:")
print(df_bfill)



data = {
    "Department": [" SALES ", "   HR", "FinanCe  ", "Sales", "MARKETING "],
    "Location": [" New York ", " Boston", "Chicago   ", "  Boston ", "LOS ANGELES"]
}
df = pd.DataFrame(data)

print("Original DataFrame:")
print(df)

# Strip whitespace
df["Department"] = df["Department"].str.strip()
df["Location"] = df["Location"].str.strip()

# Convert columns to uppercase
df["Department_upper"] = df["Department"].str.upper()
df["Location_upper"] = df["Location"].str.upper()

# Or lowercase, if you prefer
df["Department_lower"] = df["Department"].str.lower()

print("\nAfter text standardization:")
print(df)




# Sample data with dates in various formats and some invalid values
data = {
    "Event": ["Project Start", "Client Meeting", "Beta Release", "Final Launch"],
    "Date": ["2021/01/15", "2021-02-30", "03-15-2021", "April 31, 2021"]  # Some invalid or unusual dates
}
df = pd.DataFrame(data)

print("Before conversion:")
print(df)

# Convert 'Date' to datetime
# errors="coerce" will turn invalid dates into NaT (Not a Time)
df["Date_converted"] = pd.to_datetime(df["Date"], errors="coerce")

print("\nAfter converting to datetime:")
print(df)

# You can check how many values became NaT (invalid dates)
num_invalid_dates = df["Date_converted"].isna().sum()
print(f"\nNumber of invalid dates converted to NaT: {num_invalid_dates}")

#######################################
# %%

import pandas as pd
data = {'Name': ['Alice', 'Bob', 'Charlie', 'David'],
        'Age': [24, 27, 22, 32],
        'Score': [85, 92, 88, 76]}
df = pd.DataFrame(data)

print(df["Name"])
# %%
print(df.loc[0:2, ["Name", "Age"]])
# %%
print(df.iloc[:2])
# %%
print(df[df['Age'] > 24])
# print(df[df['Age'] > 24 and df['Score'] >=88])         Doesn't work!  'and' is not a valid operator for Series!
print(df[(df['Age'] > 24) & (df['Score'] >=88)])        # This one does work! It does the boolean AND of corresponding series elements.
# # print(df["a" in df['Name']])                          Doesn't work!  The "in" operator doesn't work for Series!
print(df[df['Name'].str.contains("a")])                 # This does work!  
# # There are a bunch of useful str functions for Series.  While we're at it:
# # df['Name'] = df['Name'].upper()                       Doesn't work!!
df['Name'] = df['Name'].str.upper()                     # Does work! 
print(df)
# %%
# Group data by a column and calculate the sum
data = {'Category': ['A', 'B', 'A', 'B', 'C'],
        'Values': [10, 20, 30, 40, 50]}
df = pd.DataFrame(data)

# Group by 'Category' and calculate the sum
grouped = df.groupby('Category').sum()
print(grouped) # grouped is another DataFrame with summary data

# Calculate the mean for each group
mean_values = df.groupby('Category')['Values'].mean()
print(mean_values)
# %%
import pandas as pd

# Sample DataFrame
data = {'Category': ['A', 'B', 'A', 'B', 'C'],
        'Values': [10, 20, 30, 40, 50]}
df = pd.DataFrame(data)

# Group by 'Category' and apply multiple aggregation functions
result = df.groupby('Category').agg({'Values': ['sum', 'mean', 'count']})
print(result)
# %%
# Sample DataFrames
df1 = pd.DataFrame({'ID': [1, 2, 3], 'Name': ['Alice', 'Bob', 'Charlie']})
df2 = pd.DataFrame({'ID': [1, 2, 4], 'Score': [85, 92, 88]})

# Merge on the 'ID' column
merged_df = pd.merge(df1, df2, on='ID', how='inner')
print(merged_df)  # Inner merge
# %%
import pandas as pd

# Sample DataFrames

df1 = pd.DataFrame({
    'ID': [1, 2, 3],
    'Date': ['2021-01-01', '2021-01-02', '2021-01-03'],
    'Name': ['Alice', 'Bob', 'Charlie']
})

df2 = pd.DataFrame({
    'ID': [1, 2, 3],
    'Date': ['2021-01-01', '2021-01-02', '2021-01-03'],
    'Score': [85, 92, 88]
})

# Merge on both 'ID' and 'Date'
merged_df = pd.merge(df1, df2, on=['ID', 'Date'], how='inner')
print(merged_df)
# %%
# Join DataFrames by index
df1 = pd.DataFrame({'Name': ['Alice', 'Bob', 'Charlie']}, index=[1, 2, 3])
df2 = pd.DataFrame({'Score': [85, 92, 88]}, index=[1, 2, 4])

joined_df = df1.join(df2, how='outer')
print(joined_df)
# %%
# Join DataFrames by index
df1 = pd.DataFrame({'Name': ['Alice', 'Bob', 'Charlie']}, index=[1, 2, 3])
df2 = pd.DataFrame({'Score': [85, 92, 88]}, index=[1, 2, 4])

joined_df = df1.join(df2, how='inner')
print(joined_df)
# %%
joined_df['bogus']=['x','y','z','w'] # adds a column
print(joined_df)
joined_df['bogus']=joined_df['bogus'] + "_value"  # replaces a column
print(joined_df)
joined_df.drop('bogus', axis=1, inplace=True) # deletes the column.  You need axis=1 to identify that the drop is for a column, not a row
print(joined_df)
# %%
df1 = pd.DataFrame({'Name': ['Alice', 'Bob', 'Charlie']}, index=[1, 2, 3])
df2 = pd.DataFrame({'Score': [85, 92, 88]}, index=[1, 2, 4])

joined_df = df1.join(df2, how='outer')
print(joined_df)

joined_df['bogus']=['x','y','z','w'] # adds a column
print(joined_df)
joined_df['bogus']=joined_df['bogus'] + "_value"  # replaces a column
print(joined_df)
joined_df.drop('bogus', axis=1, inplace=True) # deletes the column.  You need axis=1 to identify that the drop is for a column, not a row
print(joined_df)
# %%
df1 = pd.DataFrame({'Name': ['Alice', 'Bob', 'Charlie']}, index=[1, 2, 3])
df2 = pd.DataFrame({'Score': [85, 92, 88]}, index=[1, 2, 4])

joined_df = df1.join(df2, how='outer')
print(joined_df)

joined_df['bogus']=['x','y','z','w'] # adds a column
print(joined_df)
joined_df['bogus']=joined_df['bogus'] + "_value"  # replaces a column
print(joined_df)
joined_df.drop('bogus', axis=1, inplace=False) # deletes the column.  You need axis=1 to identify that the drop is for a column, not a row
print(joined_df)
# %%
import numpy
data = {'Name': ['A','B','C'],'Value':[1,2,3]}
new_df = pd.DataFrame(data)
print(new_df)
new_df['Value'] = new_df['Value'] ** 2  # using an operator
print(new_df)
new_df['Value'] = numpy.sqrt(new_df['Value']) # using a numpy function.  You can't use math.sqrt() on a Series.
print(new_df)
new_df['EvenOdd'] = new_df['Value'].map(lambda x : 'Even' if x % 2 == 0 else 'Odd') # the map method for a Series
print(new_df)
new_df['Value'] = new_df['Value'].astype(int) # type conversion method for a Series
print(new_df)
# %%
data1 = { 'Name': ['Alice', 'Bob', 'Charlie', 'David', 'Eva'], 'Age': [25, 30, 35, 40, 30], 'Salary': [50000, 60000, 70000, 80000, 55000] } 
data2 = { 'Name': ['Frank', 'Grace', 'Helen', 'Ian', 'Jack'], 'Age': [28, 33, 35, 29, 40], 'Salary': [52000, 58000, 72000, 61000, 85000] }
data3 = { 'Name': ['Frank', 'Helen', 'Ian', 'Hima', 'Chaka'], 'Age': [17, 93, 12, 57, 106], 'Favorite Color': ['blue', 'pink', 'burgundy', 'red', 'turquoise'] }

print(data1["Name"])
print(data1['Name', 'Salary'])

# %%
import pandas as pd
data = [{'Employee': 'Jones', 'Product': 'Widget', 'Region': 'West', 'Revenue': 9000}, \
{'Employee': 'Jones', 'Product': 'Gizmo', 'Region': 'West', 'Revenue': 4000}, \
{'Employee': 'Jones', 'Product': 'Doohickey', 'Region': 'West', 'Revenue': 11000}, \
{'Employee': 'Jones', 'Product': 'Widget', 'Region': 'East', 'Revenue': 4000}, \
{'Employee': 'Jones', 'Product': 'Gizmo', 'Region': 'East', 'Revenue': 5500}, \
{'Employee': 'Jones', 'Product': 'Doohickey', 'Region': 'East', 'Revenue': 2345}, \
{'Employee': 'Smith', 'Product': 'Widget', 'Region': 'West', 'Revenue': 9007}, \
{'Employee': 'Smith', 'Product': 'Gizmo', 'Region': 'West', 'Revenue': 40003}, \
{'Employee': 'Smith', 'Product': 'Doohickey', 'Region': 'West', 'Revenue': 110012}, \
{'Employee': 'Smith', 'Product': 'Widget', 'Region': 'East', 'Revenue': 9002}, \
{'Employee': 'Smith', 'Product': 'Gizmo', 'Region': 'East', 'Revenue': 15500}, \
{'Employee': 'Garcia', 'Product': 'Widget', 'Region': 'West', 'Revenue': 6007}, \
{'Employee': 'Garcia', 'Product': 'Gizmo', 'Region': 'West', 'Revenue': 42003}, \
{'Employee': 'Garcia', 'Product': 'Doohickey', 'Region': 'West', 'Revenue': 160012}, \
{'Employee': 'Garcia', 'Product': 'Gizmo', 'Region': 'East', 'Revenue': 16500}, \
{'Employee': 'Garcia', 'Product': 'Doohickey', 'Region': 'East', 'Revenue': 2458}]
sales = pd.DataFrame(data)
print(sales)
# %%
sales_pivot1 = pd.pivot_table(sales,index=['Product','Region'],values=['Revenue'],aggfunc='sum',fill_value=0)
print(sales_pivot1)
# This creates a two level index to show sales by product and region. The revenue values are summed for each product and region.
# %%
sales_pivot2 = pd.pivot_table(sales,index='Product',values='Revenue',columns='Region', aggfunc='sum',fill_value=0)
print(sales_pivot2)
# The result here is similar, but instead of a two level index, you have columns to give sales by region.
# %%
sales_pivot3 = pd.pivot_table(sales,index='Product',values='Revenue',columns=['Region','Employee'], aggfunc='sum',fill_value=0)
print(sales_pivot3)
# By adding the employee column, you get these revenue numbers broken down by employee.  The fill value is used when there is no corresponding entry.
# %%
sales_pivot2['Total'] = sales_pivot2['East'] + sales_pivot2['West'] # adding two columns to make a new one
print(sales_pivot2)
# %%
per_employee_sales=sales.groupby('Employee').agg({'Revenue':'sum'})
per_employee_sales['Commission Percentage'] = [0.12, 0.09, 0.1]
per_employee_sales['Commission'] = per_employee_sales['Revenue'] * per_employee_sales['Commission Percentage']
print(per_employee_sales)
# %%
def calculate_commission(row):
    if row['Revenue'] < 10000:
        return 0
    if row['Commission Plan'] == 'A':
        return 1000 + 0.05 * (row['Revenue'] - 10000)
    else:
        return 1400 + 0.04 * (row['Revenue'] - 10000)

per_employee_sales['Commission'] = per_employee_sales.apply(calculate_commission, axis=1)
print(per_employee_sales)
# %%
sales_pivot2['Total'] = sales_pivot2['East'] + sales_pivot2['West'] # adding two columns to make a new one
print(sales_pivot2)
per_employee_sales=sales.groupby('Employee').agg({'Revenue':'sum'})
per_employee_sales['Commission Percentage'] = [0.12, 0.09, 0.1]
per_employee_sales['Commission'] = per_employee_sales['Revenue'] * per_employee_sales['Commission Percentage']
print(per_employee_sales)

per_employee_sales=sales.groupby('Employee').agg({'Revenue':'sum'})
per_employee_sales['Commission Plan'] = ['A', 'A', 'B']

def calculate_commission(row):
    if row['Revenue'] < 10000:
        return 0
    if row['Commission Plan'] == 'A':
        return 1000 + 0.05 * (row['Revenue'] - 10000)
    else:
        return 1400 + 0.04 * (row['Revenue'] - 10000)

per_employee_sales['Commission'] = per_employee_sales.apply(calculate_commission, axis=1)
print(per_employee_sales)

# %%
import pandas as pd

# Sample DataFrame with missing values
data = {'Name': ['Alice', 'Bob', None, 'David'],
        'Age': [24, 27, 22, None],
        'Score': [85, None, 88, 76]}
df = pd.DataFrame(data)

# Find rows with missing data
df_missing = df[df.isnull().any(axis=1)]
print(df_missing)

# Remove rows with missing data
df_dropped = df.dropna()
print(df_dropped)

# Replace missing data with default values
df_filled = df.fillna({'Age': 0, 'Score': df['Score'].mean()})
print(df_filled)
# %%
import pandas as pd

# Sample DataFrame with mixed data types
data = {'Name': ['Alice', 'Bob', 'Charlie'],
        'Age': ['24', '27', '22'],
        'JoinDate': ['2023-01-15', '2022-12-20', '2023-03-01']}
df = pd.DataFrame(data)

# Convert 'Age' column to integers
df['Age'] = df['Age'].astype(int)

# Convert 'JoinDate' column to datetime
df['JoinDate'] = pd.to_datetime(df['JoinDate'])

print(df.dtypes)  # Verify data types
print(df)
# %%
import pandas as pd

# Sample DataFrame

data = {'Name': ['Alice', 'Bob', 'Charlie'],
        'Location': ['LA', 'LA', 'NY'],
        'JoinDate': ['2023-01-15', '2022-12-20', '2023-03-01']}
df = pd.DataFrame(data)

# Convert 'Location' abbreviations into full names

df['Location'] = df['Location'].map({'LA': 'Los Angeles', 'NY': "New York"})
print(df)
# %%
import pandas as pd
data = {'Name': ['Tom', 'Dick', 'Harry', 'Mary'], 'Phone': [3212347890, '(212)555-8888', '752-9103','8659134568']}
df = pd.DataFrame(data)
df['Correct Phone'] = df['Phone'].astype(str)

def fix_phone(phone):
    if phone.isnumeric():
        out_string = phone
    else:
        out_string = ''
        for c in phone:
            if c in '0123456789':
                out_string += c
    if len(out_string) == 10:
        return out_string
    return None
    
df['Correct Phone'] = df['Correct Phone'].map(fix_phone)
print(df)
# %%
# import pandas as pd

# data = {'Name': ['Alice', 'Bob', 'Charlie'],
# 	'Age': [20, 22, 43]}

# df = pd.DataFrame(data)

# # Increase the age by 1 as a new year has passed
# # df['Age'] = df['Age'] += 1
# # print(df)

import pandas as pd
data = {'Name': ['Alice', 'Bob', 'Charlie'],
        'Location': ['LA', 'LA', 'NY'],
        'Grade': [78, 40, 85]}
df = pd.DataFrame(data)

# Convert grade into three catagories, "bad", "okay", "great"

df['Grade'] = pd.cut(df['Grade'], 3, labels = ["bad", "okay", "great"])
print(df)
# %%
import pandas as pd

# Sample DataFrame with duplicates
data = {'Name': ['Alice', 'Bob', 'Alice', 'David'],
        'Age': [24, 27, 24, 32],
        'Score': [85, 92, 85, 76]}
df = pd.DataFrame(data)

# Identify and remove duplicates
# df_cleaned = df.drop_duplicates()
# print(df_cleaned)

# # Remove duplicates based on 'Name' column
df_cleaned_by_name = df.drop_duplicates(subset='Name')
print(df_cleaned_by_name)
# %%
