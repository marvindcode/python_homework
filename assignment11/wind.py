import plotly.express as px
import plotly.data as pldata
import pandas as pd

df = pldata.wind(return_type='pandas')

print("First 10 rows:\n", df.head(10))
print("Last 10 rows:\n", df.tail(10))

df['strength'] = df['strength'].str.replace(r'\D', '', regex=True)

df['strength'] = pd.to_numeric(df['strength'], errors='coerce')

df = df.dropna(subset=['strength'])

fig = px.scatter(df, x='frequency', y='strength', color='direction', title='Wind Strength vs Frequency')

fig.show()
