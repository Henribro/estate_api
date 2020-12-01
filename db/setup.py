import sqlite3


conn = sqlite3.connect('estate.db')

cursor = conn.cursor()

#Create table users
cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
    name TEXT,
    first_name TEXT,
    date_of_birth INTEGER
)
""")

#Create table properties
cursor.execute("""
CREATE TABLE IF NOT EXISTS properties(
    id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
    name TEXT,
    surface_area INTEGER,
    date_of_birth INTEGER
)
""")


conn.commit()





conn.close()
