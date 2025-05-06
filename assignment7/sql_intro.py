#%%
# Task 1: Create a New SQLite Database
import sqlite3

def new_database():
    try:
        connect = sqlite3.connect("../db/magazines.db") 
        print("Database created and connected successfully.")
    
    except sqlite3.IntegrityError:
        print(f"An error occurrred in database")

# %%
# Task 2: Define Database Structure

# 1.The table that has a foreign key is the magazine  because a publisher will have an id_publisher that will be primary key on his table but foreign key in magazine.  The subscriptions table will have a primary key of ID_Magazine that will be foreign on the Magazines table and also will have a foreign key from subscribers like ID_subscriber.

#2. Add SQL statements to sql_intro.py that create the following tables:
# publishers
# magazines
# subscribers
# subscriptions 
# Be sure to include the columns you need in each, with the right data types, with UNIQUE and NOT NULL constraints as needed, and with foreign keys as needed. You can reuse column names if you choose, i.e. you might have a name column for publishers and a name column for magazines. By the way, if you mess up this or the following steps, you can just delete db/magazines.db.

#3. Open the db/magazines.db file in VSCode to confirm that the tables are created.
# %%
import sqlite3

def new_database():
    try:
        connect = sqlite3.connect("../db/magazines.db") 
        cursor = connect.cursor()
        print("Database created and connected successfully.")
    
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Publishers (
            publisher_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL UNIQUE
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Magazines (
                magazine_id INTEGER PRIMARY KEY,
                name TEXT NOT NULL UNIQUE,
                publisher_id INTEGER NOT NULL,
                FOREIGN KEY (publisher_id) REFERENCES Publishers (publisher_id)
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Subscribers (
                subscriber_id INTEGER PRIMARY KEY,
                name TEXT NOT NULL UNIQUE,
                age INTEGER,
                email TEXT NOT NULL UNIQUE
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Subscriptions (
                subscription_id INTEGER PRIMARY KEY,
                subscriber_id INTEGER NOT NULL,
                magazine_id INTEGER NOT NULL,
                FOREIGN KEY (magazine_id) REFERENCES Magazines (magazine_id),
                FOREIGN KEY (subscriber_id) REFERENCES Subscribers (subscriber_id)
        )
        """)

        connect.commit()
        print ("Tables created successfully.")
    
    except sqlite3.IntegrityError:
        print(f"An error occurrred in database")

if __name__ == "__main__":
    new_database()

# %%
#Task 3: Populate Tables with Data

#1. Add the following line to sql_intro.py, right after the statement that connects to the database:
#conn.execute("PRAGMA foreign_keys = 1")
# This line tells SQLite to make sure the foreign keys are valid.

#2. Create functions, one for each of the tables, to add entries. Include code to handle exceptions as needed, and to ensure that there is no duplication of information. The subscribers name and address columns don't have unique values -- you might have several subscribers with the same name -- but when creating a subscriber you should check that you don't already have an entry where BOTH the name and the address are the same as for the one you are trying to create.
#3. Add code to the main line of your program to populate each of the 4 tables with at least 3 entries. Don't forget the commit!
#4. Run the program several times. View the database to ensure that you are creating the right information, without duplication.
import sqlite3

def add_publisher(cursor, name):
    try:
        cursor.execute("INSERT INTO Publishers (name) VALUES (?)", (name,))
    except sqlite3.IntegrityError:
        print(f"Publisher '{name}' is already in the database.")

 
def add_magazine(cursor, name, publisher_id):
    try:
        cursor.execute("INSERT INTO Magazines (name, publisher_id) VALUES (?, ?)", (name, publisher_id))
    except sqlite3.IntegrityError:
        print(f"Magazine '{name}' is already in the database.") 

def add_subscriber(cursor, name, age, email):
    try:
        cursor.execute("INSERT INTO Subscribers (name, age, email) VALUES (?, ?, ?)", (name, age, email)) 
    except sqlite3.IntegrityError:
        print(f"Subscriber '{name}' with '{age}' and '{email}' already exists in the database.") 

def add_subscription(cursor, subscriber_id, magazine_id):
    try:
        cursor.execute("INSERT INTO Subscriptions (subscriber_id, magazine_id) VALUES (?, ?)", (subscriber_id, magazine_id))
    except sqlite3.IntegrityError:
        print(f"Subscription added for subscriber '{subscriber_id}' to magazine '{magazine_id}' already exists in the database.") 
    
def add_sample_data(cursor):
 
    add_publisher(cursor, "O'Reilly Media")
    add_publisher(cursor, "Getty Publications")
    add_publisher(cursor, "Ebony")
    add_publisher(cursor, "Fast Company")

    add_magazine(cursor, "Us Weekly", 1)
    add_magazine(cursor, "TIME Magazine", 2)
    add_magazine(cursor, "Reader's Digest", 3) 
    add_magazine(cursor, "Real Simple", 4)  
    
    add_subscriber(cursor, "Michael Kane", 45, "mkane@yahoo.com")
    add_subscriber(cursor, "Charlie Stewart", 35, "charlies@gmail.com")
    add_subscriber(cursor, "Michelle Harrington", 28, "Micharris@live.com")
    add_subscriber(cursor, "Ann Hateway", 63, "annhateway@aol.com")

    add_subscription(cursor, 1, 1)
    add_subscription(cursor, 2, 2)
    add_subscription(cursor, 3, 3)
    add_subscription(cursor, 4, 4)

def new_database():
    with sqlite3.connect("../db/magazines.db") as conn:
        conn.execute("PRAGMA foreign_keys = 1")
        cursor = conn.cursor()

        add_sample_data(cursor)
    
        conn.commit()
        print("Data inserted successfully.")

if __name__ == "__main__":
    new_database()  

# %%
# Task 4: Write SQL Queries
# Write a query to retrieve all information from the subscribers table.
# Write a query to retrieve all magazines sorted by name.
# Write a query to find magazines for a particular publisher, one of the publishers you created. This requires a JOIN.
# Add these queries to your script. For each, print out all the rows returned by the query.

def run_queries(cursor):
    cursor.execute("SELECT * FROM Subscribers;")
    result = cursor.fetchall()
    for row in result:
        print(row)

    cursor.execute("SELECT * FROM Magazines ORDER BY name;")
    result = cursor.fetchall()
    for row in result:
        print(row) 

    cursor.execute("""
        SELECT Magazines.*
        FROM Magazines 
        JOIN Publishers ON Magazines.publisher_id = Publishers.publisher_id 
        WHERE Publishers.name = ?;
    """, ("Fast Company",))
    result = cursor.fetchall()
    for row in result:
        print(row)  

def new_database():
    with sqlite3.connect("../db/magazines.db") as conn:
        conn.execute("PRAGMA foreign_keys = 1")
        cursor = conn.cursor()

        run_queries(cursor)

if __name__ == "__main__":
    new_database()



