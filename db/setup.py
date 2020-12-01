import sqlite3
import os

conn = sqlite3.connect("estate.db")

cursor = conn.cursor()

#Create table users
cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
    name TEXT NOT NULL,
    first_name TEXT NOT NULL
);





""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS properties(
    id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
    user_id INTEGER,
    FOREIGN KEY(user_id) REFERENCES users(id)
    name TEXT,
    location TEXT,
    surface_area INTEGER
);
""")


#Create table properties
# cursor.execute("""
#
# """)

# #Add Henri Brault user
# cursor.execute("INSERT INTO users (name,first_name) VALUES ('Brault','Henri')")
#
# cursor.execute("SELECT * FROM users")
# print(cursor.fetchone())

conn.commit()
conn.close()