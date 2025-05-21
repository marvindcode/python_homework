# %%
import sqlite3

with sqlite3.connect("../db/lesson.db") as conn:
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM products ORDER BY product_name;")
    for row in cursor.fetchall():
        print(row)

    cursor.execute("""
        SELECT orders.order_id, customers.customer_name
        FROM orders
        JOIN customers ON orders.customer_id = customers.customer_id;
    """)
    for row in cursor.fetchall():
        print(row)

    cursor.execute("""
        SELECT line_item_id, SUM(quantity) AS total_qty
        FROM line_items
        GROUP BY product_id
        HAVING total_qty > 50;
    """)
    for row in cursor.fetchall():
        print(row)

# %%
