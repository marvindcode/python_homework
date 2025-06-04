import pandas as pd

df = pd.read_csv('Procurement KPI Analysis Dataset.csv')  

print(df.head())

df["Order_Date"] = pd.to_datetime(df["Order_Date"])
df["Delivery_Date"] = pd.to_datetime(df["Delivery_Date"])

df["Defective_Units"].fillna(0, inplace=True)

df["Delivery_Date"].fillna(pd.NaT, inplace=True)

print(df.head())
print(df.info())
print(df.isnull().sum())

df.to_csv("cleaned_procurement_data.csv", index=False)

