import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# DB connection
def load_data():
    conn = sqlite3.connect("mlb_data.db")
    history = pd.read_sql("SELECT * FROM series_history", conn)
    receipts = pd.read_sql("SELECT * FROM gate_receipts", conn)
    conn.close()
    return history, receipts

df_history, df_receipts = load_data()

# Sidebar and filtering
st.sidebar.title("MLB World Series Dashboard")
st.sidebar.markdown("Use the slider to filter data by year range.")
year_range = st.sidebar.slider("Select Year Range", int(df_history["Year"].min()), int(df_history["Year"].max()), (1950, 2023))
filtered_history = df_history[df_history["Year"].between(*year_range)]
filtered_receipts = df_receipts[df_receipts["Year"].between(*year_range)]

# Title
st.title("MLB World Series Insights (1903–2023)")
st.markdown("""
Use the sidebar to select a range of years and explore key insights below.  
This dashboard includes gate receipts, ticket pricing trends, team performance, and attendance statistics.
""")

# Chart 1: Yearly Gate Receipts
st.subheader("1. Yearly Gate Receipts")
st.markdown("""
This chart shows how much revenue MLB generated from gate receipts for each World Series.  
Revenue has increased in recent decades due to rising ticket prices and stadium capacities.
""")
fig1, ax1 = plt.subplots()
ax1.plot(filtered_receipts["Year"], filtered_receipts["Gate Receipts"])
ax1.set_ylabel("Gate Receipts ($)")
ax1.set_xlabel("Year")
st.pyplot(fig1)

# Chart 2: Average Ticket Price Proxy
st.subheader("2. Average Ticket Price (Gate Receipts ÷ Attendance)")
st.markdown("""
This graph is calculated as Gate Receipts divided by Attendance to get average ticket price.
It shows how price has increased over the time.
""")
df_avg_ticket = filtered_receipts.copy()
df_avg_ticket["Avg Ticket Price"] = df_avg_ticket["Gate Receipts"] / df_avg_ticket["Attendance"]
fig2, ax2 = plt.subplots()
ax2.plot(df_avg_ticket["Year"], df_avg_ticket["Avg Ticket Price"])
ax2.set_ylabel("Estimated Ticket Price ($)")
ax2.set_xlabel("Year")
st.pyplot(fig2)

# Chart 3: Teams by Appearances, Wins and Losses, and Top 10 attendance years
st.subheader("3. Top Teams by World Series Appearances and Wins")

option = st.selectbox(
    "Select view:",
    ("Appearances", "Wins", "Losses", "Top 10 Attendance Years", "Most Common Games Played")
)

# Appearances
if option == "Appearances":
    st.markdown("""
    Which teams have played the most World Series?  
    This graph shows the top 10 teams by total appearances.
    """)
    teams = pd.concat([filtered_history["American League"], filtered_history["National League"]])
    appearance_counts = teams.value_counts().sort_values(ascending=True).tail(10)
    fig, ax = plt.subplots()
    ax.barh(appearance_counts.index, appearance_counts.values)
    ax.set_xlabel("Total Appearances")
    ax.set_title("Top 10 Teams by Appearances")
    st.pyplot(fig)

# Wins
elif option == "Wins":
    st.markdown("""
    Which teams have won the most World Series titles?  
    This chart counts the number of times a team have won the World Series titles.
    """)
    winners = filtered_history.apply(
        lambda row: row["American League"] if row["AL Wins"] > row["NL Wins"] else row["National League"],
        axis=1
    )
    win_counts = winners.value_counts().sort_values(ascending=True).tail(10)
    fig, ax = plt.subplots()
    ax.barh(win_counts.index, win_counts.values)
    ax.set_xlabel("Total Wins")
    ax.set_title("Top 10 Teams by Wins")
    st.pyplot(fig)

# Losses
elif option == "Losses":
    st.markdown("""
    Which teams have lost the most in the World Series?  
    This chart shows the teams that appeared most times but have lost the series.
    """)
    losers = filtered_history.apply(
        lambda row: row["American League"] if row["AL Wins"] < row["NL Wins"] else row["National League"],
        axis=1
    )
    loss_counts = losers.value_counts().sort_values(ascending=True).tail(10)
    fig, ax = plt.subplots()
    ax.barh(loss_counts.index, loss_counts.values)
    ax.set_xlabel("Total Losses")
    ax.set_title("Top 10 Teams by Losses")
    st.pyplot(fig)

# Attendance
elif option == "Top 10 Attendance Years":
    st.markdown("""
    This chart shows which years had the highest World Series attendance.  
    Higher attendance factors could be: bigger stadiums, team popularity, and extended series.
    """)
    df_receipts = df_receipts.dropna(subset=["Attendance", "Year"])
    df_receipts["Attendance"] = pd.to_numeric(df_receipts["Attendance"], errors="coerce")
    top_attendance = df_receipts.sort_values(by="Attendance", ascending=False).head(10)
    fig, ax = plt.subplots()
    ax.barh(top_attendance["Year"].astype(str), top_attendance["Attendance"])
    ax.set_xlabel("Attendance")
    ax.set_title("Top 10 Years by World Series Attendance")
    ax.invert_yaxis()
    st.pyplot(fig)

# Most Common Number of Games Played
elif option == "Most Common Games Played":
    st.markdown("""
    This chart shows how often World Series lasted 4, 5, 6, or 7 games.  
    To win the World Seeries, a team needs to 4 games, in a best of 7. 
    Note: the first World Series in 1903 it was a best of 9 series.
    """)
    games_count = filtered_receipts["Games"].value_counts().sort_index()
    fig, ax = plt.subplots()
    ax.bar(games_count.index.astype(str), games_count.values)
    ax.set_xlabel("Games in Series")
    ax.set_ylabel("Number of Times Occurred")
    ax.set_title("Most Common Number of Games Played in World Series")
    st.pyplot(fig)

def get_league_win_comparison(df):
    nl_total = df["NL Wins"].sum()
    al_total = df["AL Wins"].sum()

    if nl_total > al_total:
        winner = "National League"
    elif al_total > nl_total:
        winner = "American League"
    else:
        winner = "It's a tie!"

    return nl_total, al_total, winner

# League Wins Summary
st.subheader("League Comparison: Which League has more wins (Selected Years)?")
nl_wins, al_wins, leading_league = get_league_win_comparison(filtered_history)
st.markdown(f"""
**Total Wins (From {year_range[0]} to {year_range[1]})**  
- National League: `{nl_wins}`  
- American League: `{al_wins}`  
- **{leading_league}** has won more World Series.
""")

# League Wins Graph: Pie chart
fig_pie, ax_pie = plt.subplots()
ax_pie.pie(
    [nl_wins, al_wins],
    labels=["National League", "American League"],
    autopct="%1.1f%%",
    startangle=90,
    colors=["#FF4136", "#0074D9"]
)
ax_pie.axis("equal")
st.pyplot(fig_pie)

# Sidebar leagua wins
st.sidebar.markdown("### League Wins")
st.sidebar.markdown(f"- NL Wins: `{nl_wins}`")
st.sidebar.markdown(f"- AL Wins: `{al_wins}`")
st.sidebar.markdown(f"**{leading_league} leads**")