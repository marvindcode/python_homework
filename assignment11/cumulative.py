import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

with sqlite3.connect("../db/lesson.db") as conn:
    cursor = conn.cursor()

query = '''
SELECT o.order_id, SUM(price * quantity) AS total_price
FROM orders o
JOIN line_items l ON o.order_id = l.order_id
JOIN products p ON l.product_id = p.product_id
GROUP BY o.order_id;
'''

df = pd.read_sql(query, conn)
1.db
df['cumulative'] = df['total_price'].cumsum()

df.plot(x='order_id', y='cumulative', kind='line', color='black')
plt.title('Revenue per Order')
plt.xlabel('Order ID')
plt.ylabel('Cumulative Revenue')
plt.show()
