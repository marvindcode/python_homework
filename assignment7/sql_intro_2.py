
#%%
#Task 5: Read Data into a DataFrame

# You will now use Pandas to create summary data from the ../db/lesson.db database you populated as part of the lesson.  We want to find out how many times each product has been ordered, and what was the total price paid by product.
# While still within the python_homework/assignment7 directory, create a program, sql_intro_2.py.
# Read data into a DataFrame, as described in the lesson. The SQL statement should retrieve the line_item_id, quantity, product_id, product_name, and price from a JOIN of the line_items table and the product table. Hint: Your ON statement would be ON line_items.product_id = products.product_id.
# Print the first 5 lines of the resulting DataFrame. Run the program to make sure this much works.
# Add a column to the DataFrame called "total". This is the quantity times the price. (This is easy: df['total'] = df['quantity'] * df['price'].) Print out the first 5 lines of the DataFrame to make sure this works.

# Add groupby() code to group by the product_id. Use an agg() method that specifies 'count' for the line_item_id column, 'sum' for the total column, and 'first' for the 'product_name'. Print out the first 5 lines of the resulting DataFrame. Run the program to see if it is correct so far.
# Sort the DataFrame by the product_name column.
# Add code to write this DataFrame to a file order_summary.csv, which should be written in the assignment7 directory. Verify that this file is correct.
# As we'll learn in the next lesson, the ordering, grouping, count, and sum operations can be done in SQL, more efficiently than in Pandas.  The key concepts of pandas and SQL overlap very strongly.

import pandas as pd
import sqlite3

with sqlite3.connect("../db/lesson.db") as conn:
    sql_statement = """
    SELECT 
        li.line_item_id,
        li.quantity,
        li.product_id,
        p.product_name,
        p.price
    FROM line_items li
    JOIN products p ON li.product_id = p.product_id
    """

df = pd.read_sql_query(sql_statement, conn)
print(df.head())

df['total'] = df['quantity'] * df['price']
print(df.head())

grupo = df.groupby('product_id').agg({
    'line_item_id': 'count',       
    'total': 'sum',               
    'product_name': 'first'       
}).reset_index()

print(grupo.head())

grupo = grupo.sort_values(by='product_name')

grupo.to_csv("order_summary.csv", index=False)


# %%
