# Task 1: Complex JOINs with Aggregation

# Problem Statement:

# Find the total price of each of the first 5 orders.  There are several steps.  You need to join the orders table with the line_items table and the products table.  You need to GROUP_BY the order_id.  You need to select the order_id and the SUM of the product price times the line_item quantity.  Then, you ORDER BY order_id and LIMIT 5.  You don't need a subquery. Print out the order_id and the total price for each of the rows returned.

# Deliverable:

# Within the python_homework folder, create an assignment8 branch. Change to the assignment8 folder.
# Get the SQL statement working in sqlcommand.
# Within the assignment8 folder, create advanced_sql.py. This should open the database, issue the SQL statement, print out the result, and close the database.
# test your program.
# %%
import sqlite3

def total_first_orders():
    with sqlite3.connect("../db/lesson.db") as conn:
        cursor = conn.cursor()

        query = """
        SELECT
            o.order_id,
            SUM(li.quantity * p.price) AS total_price

        FROM orders o
        JOIN line_items li ON o.order_id = li.order_id
        JOIN products p ON li.product_id = p.product_id
        GROUP BY o.order_id
        ORDER BY o.order_id
        LIMIT 5;
        """

        cursor.execute(query)
        results = cursor.fetchall()
        print(results)

if __name__ == "__main__":
    total_first_orders()
# %%
# Task 2: Understanding Subqueries

# Problem Statement:

# For each customer, find the average price of their orders.  This can be done with a subquery. You compute the price of each order as in part 1, but you return the customer_id and the total_price.  That's the subquery. You need to return the total price using AS total_price, and you need to return the customer_id with AS customer_id_b, for reasons that will be clear in a moment.  In your main statement, you left join the customer table with the results of the subquery, using ON customer_id = customer_id_b.  You aliased the customer_id column in the subquery so that the column names wouldn't collide.  Then group by customer_id -- this GROUP BY comes after the subquery -- and get the average of the total price of the customer orders.  Return the customer name and the average_total_price.

# Deliverable:

# Again, get the SQL statement working in sqlcommand.
# Add code to advanced_sql.py to print out the result.

import sqlite3

def customer_avg_price():
    with sqlite3.connect("../db/lesson.db") as conn:
        cursor = conn.cursor()


        query = """
        SELECT
            c.customer_name,
            AVG(order_totals.total_price) AS average_total_price
        FROM customers c
        LEFT JOIN (
            SELECT
                o.customer_id AS customer_id_b,
                o.order_id,
                SUM(li.quantity * p.price) AS total_price
            FROM orders o
            JOIN line_items li ON o.order_id = li.order_id
            JOIN products p ON li.product_id = p.product_id
            GROUP BY o.order_id
        ) AS order_totals
        ON c.customer_id = order_totals.customer_id_b
        GROUP BY c.customer_id
        ORDER BY c.customer_name;
        """

        cursor.execute(query)
        results = cursor.fetchall()
        print(results)

if __name__ == "__main__":
    customer_avg_price()
# %%
#Task 3: An Insert Transaction Based on Data

# 1. Problem Statement:

# You want to create a new order for the customer named Perez and Sons.  The employee creating the order is Miranda Harris.  The customer wants 10 of each of the 5 least expensive products.  You first need to do a SELECT statement to retrieve the customer_id, another to retrieve the product_ids of the 5 least expensive products, and another to retrieve the employee_id.  Then, you create the order record and the 5 line_item records comprising the order.  You have to use the customer_id, employee_id, and product_id values you obtained from the SELECT statements. You have to use the order_id for the order record you created in the line_items records. The inserts must occur within the scope of one transaction. Then, using a SELECT with a JOIN, print out the list of line_item_ids for the order along with the quantity and product name for each.

# You want to make sure that the foreign keys in the INSERT statements are valid.  So, add this line to your script, right after the database connection:

    # conn.execute("PRAGMA foreign_keys = 1")

# In general, when creating a record, you don't want to specify the primary key.  So leave that column name off your insert statements.  SQLite will assign a unique primary key for you.  But, you need the order_id for the order record you insert to be able to insert line_item records for that order.  You can have this value returned by adding the following clause to the INSERT statement for the order:

    # RETURNING order_id

# 2. Deliverable:
# Get this working in sqlcommand. (Note that sqlcommand does not provide a way to begin and end transactions, so for sqlcommand, the creation of the order and line_item records are separate transactions.)
# Use sqlcommand to delete the line_items records for the order you created. (This is one delete statement.) Delete also the order record you created.
# Add statements for the complete transaction and the subsequent SELECT statement into advanced_py.sql, and to print out the result of the SELECT.
# Test your program.

import sqlite3

def new_order():
    with sqlite3.connect("../db/lesson.db") as conn:
        conn.execute("PRAGMA foreign_keys = 1")
        cursor = conn.cursor()

        cursor.execute("SELECT customer_id FROM customers WHERE customer_name = 'Perez and Sons';")
        customer_id = cursor.fetchone()[0]

        cursor.execute("SELECT employee_id FROM employees WHERE first_name = 'Miranda' AND last_name = 'Harris';")
        employee_id = cursor.fetchone()[0]

        cursor.execute("SELECT product_id FROM products ORDER BY price LIMIT 5;")
        product_ids = [row[0] for row in cursor.fetchall()]

        try:
            cursor.execute("""
                INSERT INTO orders (customer_id, employee_id)
                VALUES (?, ?)
                RETURNING order_id;
            """, (customer_id, employee_id))
            order_id = cursor.fetchone()[0]

            for product_id in product_ids:
                cursor.execute("""
                    INSERT INTO line_items (order_id, product_id, quantity)
                    VALUES (?, ?, ?);
                """, (order_id, product_id, 10))

            conn.commit()

        except Exception as e:
            print("Error occurred:", e)
            return

        cursor.execute("""
            SELECT li.line_item_id, li.quantity, p.product_name
            FROM line_items li
            JOIN products p ON li.product_id = p.product_id
            WHERE li.order_id = ?;
        """, (order_id,))

        results = cursor.fetchall()
        for line_item_id, quantity, product_name in results:
            print(line_item_id, quantity, product_name)
        
        
if __name__ == "__main__":
    new_order()

# %%
# Task 4: Aggregation with HAVING

# 1. Problem Statement:

# Find all employees associated with more than 5 orders.  You want the first_name, the last_name, and the count of orders.  You need to do a JOIN on the employees and orders tables, and then use GROUP BY, COUNT, and HAVING.

# 2. Deliverable:

# Get it working in sqlcommand.
# Add code advanced_sql.py to print out the employee_id, first_name, last_name, and an order count for each of the employees with more than 5 orders.
# Test your program.

import sqlite3

def find_employees_over5orders():
    with sqlite3.connect("../db/lesson.db") as conn:
        cursor = conn.cursor()

        query = """
        SELECT 
            e.employee_id,
            e.first_name,
            e.last_name,
            COUNT(o.order_id) AS order_count
        FROM employees e
        JOIN orders o ON e.employee_id = o.employee_id
        GROUP BY e.employee_id
        HAVING COUNT(o.order_id) > 5
        ORDER BY order_count DESC;
        """

        cursor.execute(query)
        results = cursor.fetchall()
        print(results)

if __name__ == "__main__":
    find_employees_over5orders()

# %%
