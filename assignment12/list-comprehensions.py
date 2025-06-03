import pandas as pd

df = pd.read_csv("../csv/employees.csv")

list_employees = [f"{row['first_name']} {row['last_name']}" for _, row in df.iterrows()]
print(list_employees)

list_with_e = [name for name in list_employees if "e" in name]
print(list_with_e)
