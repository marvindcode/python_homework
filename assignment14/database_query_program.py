import pandas as pd
import sqlite3
import os

# DAta to load
DB_NAME = "mlb_data.db"
HISTORY_CSV = "clean_world_series_history.csv"
RECEIPTS_CSV = "clean_world_series_receipts.csv"

# Load cleaned CSVs
df_history = pd.read_csv(HISTORY_CSV)
df_receipts = pd.read_csv(RECEIPTS_CSV)

# Creating SQLite DB
conn = sqlite3.connect(DB_NAME)

# Tables
try:
    df_history.to_sql("series_history", conn, if_exists="replace", index=False)
    df_receipts.to_sql("gate_receipts", conn, if_exists="replace", index=False)
except Exception as e:
    print("Error writing to SQLite:", e)
    conn.close()
    exit(1)

# Checking sample data
print(df_history.head(5))

print(df_receipts.head(5))

# Close connection
conn.close()


def connect_db():
    return sqlite3.connect("mlb_data.db")

def avg_ticket_price():
    conn = connect_db()
    query = """
        SELECT Year, 
               ROUND("Gate Receipts" / Attendance, 2) AS Avg_Ticket_Price
        FROM gate_receipts
        WHERE "Gate Receipts" IS NOT NULL AND Attendance IS NOT NULL
        ORDER BY Year
    """
    df = pd.read_sql(query, conn)
    print(df)
    conn.close()

def series_length_effect():
    conn = connect_db()
    query = """
        SELECT 
            Games,
            ROUND(AVG("Gate Receipts"), 2) AS Avg_Receipts
        FROM gate_receipts
        WHERE Games IS NOT NULL AND "Gate Receipts" IS NOT NULL
        GROUP BY Games
        ORDER BY Games
    """
    df = pd.read_sql(query, conn)
    print(df)
    conn.close()

def players_revenue_pct():
    conn = connect_db()
    query = """
        SELECT Year,
               ROUND(("Players' Total" * 100.0) / "Gate Receipts", 2) AS Player_Revenue_Pct
        FROM gate_receipts
        WHERE "Players' Total" IS NOT NULL AND "Gate Receipts" IS NOT NULL
        ORDER BY Year
    """
    df = pd.read_sql(query, conn)
    print(df)
    conn.close()

def yearly_gate_trend():
    conn = connect_db()
    query = """
        SELECT Year, "Gate Receipts"
        FROM gate_receipts
        WHERE "Gate Receipts" IS NOT NULL
        ORDER BY Year
    """
    df = pd.read_sql(query, conn)
    print(df)
    conn.close()

def common_games_played():
    conn = connect_db()
    query = """
        SELECT Games, COUNT(*) AS Series_Count
        FROM gate_receipts
        WHERE Games IS NOT NULL
        GROUP BY Games
        ORDER BY Series_Count DESC
        LIMIT 5
    """
    df = pd.read_sql(query, conn)
    print(df)
    conn.close()

def most_series_appearances():
    conn = connect_db()
    query = """
        SELECT "National League" AS Team, COUNT(*) AS Appearances
        FROM series_history
        WHERE "National League" NOT LIKE 'No Series%'
        GROUP BY "National League"
        UNION ALL
        SELECT "American League", COUNT(*)
        FROM series_history
        WHERE "American League" NOT LIKE 'No Series%'
        GROUP BY "American League"
    """
    df = pd.read_sql(query, conn)
    df = df.groupby("Team").sum().sort_values(by="Appearances", ascending=False).reset_index()
    print(df.head(10))
    conn.close()

def most_world_series_wins():
    conn = connect_db()
    query = """
        SELECT "National League" AS Team, SUM("NL Wins") AS Wins
        FROM series_history
        GROUP BY "National League"
        UNION ALL
        SELECT "American League", SUM("AL Wins")
        FROM series_history
        GROUP BY "American League"
    """
    df = pd.read_sql(query, conn)
    df = df.groupby("Team").sum().sort_values(by="Wins", ascending=False).reset_index()
    print(df.head(10))
    conn.close()

def top_attendance_years():
    conn = connect_db()
    query = """
        SELECT Year, Attendance
        FROM gate_receipts
        WHERE Attendance IS NOT NULL
        ORDER BY Attendance DESC
        LIMIT 10
    """
    df = pd.read_sql(query, conn)
    print(df)
    conn.close()

def compare_league_wins():
    conn = connect_db()

    query = """
        SELECT 
            SUM("NL Wins") AS NL_Total_Wins,
            SUM("AL Wins") AS AL_Total_Wins
        FROM series_history
    """
    df = pd.read_sql(query, conn)
    conn.close()

    nl_wins = df["NL_Total_Wins"].iloc[0]
    al_wins = df["AL_Total_Wins"].iloc[0]

    print(f"National League Total Wins: {nl_wins}")
    print(f"American League Total Wins: {al_wins}")  

def main():
    while True:
        print("""
Choose an option:
1. Show average ticket price by year
2. Show gate receipts vs. number of games 
3. Show players' revenue percentage over time
4. Show yearly gate receipts trend
5. Most common number of games played
6. Teams with most World Series appearances
7. Teams with most World Series wins
8. Top 10 attendance years
9. Compare total wins by league
10. Exit
        """)
        choice = input("Enter your choice: ")
        if choice == "1":
            avg_ticket_price()
        elif choice == "2":
            series_length_effect()
        elif choice == "3":
            players_revenue_pct()
        elif choice == "4":
            yearly_gate_trend()
        elif choice == "5":
            common_games_played()
        elif choice == "6":
            most_series_appearances()
        elif choice == "7":
            most_world_series_wins()
        elif choice == "8":
            top_attendance_years()
        elif choice == "9":
            compare_league_wins()
        elif choice == "10":
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
