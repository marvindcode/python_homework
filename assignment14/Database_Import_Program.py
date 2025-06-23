import pandas as pd

# Load the world_series_history file
df = pd.read_csv("world_series_history.csv")

# Remove repeated header rows
df = df[df["Year"].astype(str).str.match(r"^\d{4}$")].reset_index(drop=True)

# Clean team names (removed metadata)
df["National League"] = df["National League"].astype(str).str.split("\n").str[0].str.strip()
df["American League"] = df["American League"].astype(str).str.split("\n").str[0].str.strip()

# Convert data types
df["Year"] = df["Year"].astype(int)
df["NL Wins"] = pd.to_numeric(df["NL Wins"], errors="coerce").astype("Int64")
df["AL Wins"] = pd.to_numeric(df["AL Wins"], errors="coerce").astype("Int64")

print(df.head(10))
print(df.info())

# Save cleaned worls_series_history
df.to_csv("clean_world_series_history.csv", index=False)



# Load the world_series_receipts file
df1 = pd.read_csv("world_series_receipts.csv")

# Remove repeated header rows
df1 = df1[df1["Year"].astype(str).str.match(r"^\d{4}$")].reset_index(drop=True)

# Converted numeric fields
df1["Year"] = df1["Year"].astype(int)
df1["Games"] = pd.to_numeric(df1["Games"], errors="coerce").astype("Int64")

# For Attendance was necessary to remove commas and convert to float
df1["Attendance"] = pd.to_numeric(
    df1["Attendance"].astype(str).str.replace(",", "").str.replace("--", ""),
    errors="coerce"
)

# For the currency fields was necessary to clean them
currency_fields = ["Gate Receipts", "Players' Total", "Winners", "Losers"]
for col in currency_fields:
    df1[col] = pd.to_numeric(
        df1[col].astype(str).str.replace(r"[\$,]", "", regex=True).str.replace("--", ""),
        errors="coerce"
    )

print(df1.head(10))
print(df1.info())

# Save cleaned world_series_receipts
df1.to_csv("clean_world_series_receipts.csv", index=False)

