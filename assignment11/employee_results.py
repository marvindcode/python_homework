# %%
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

with sqlite3.connect("../db/lesson.db") as conn:
    cursor = conn.cursor()

query = '''
SELECT last_name, SUM(price * quantity) AS revenue
FROM employees e
JOIN orders o ON e.employee_id = o.employee_id
JOIN line_items l ON o.order_id = l.order_id
JOIN products p ON l.product_id = p.product_id
GROUP BY e.employee_id;
'''

df = pd.read_sql(query, conn)

df.plot(kind='bar', x='last_name', y='revenue', color='red')
plt.title('Employee Revenue')
plt.xlabel('Employee Last Name')
plt.ylabel('Revenue')
plt.show()

# %%
