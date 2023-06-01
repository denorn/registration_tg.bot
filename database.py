import sqlite3

conn = sqlite3.connect('users.db')

conn.execute('''CREATE TABLE IF NOT EXISTS users
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              chat_id INTEGER,
              first_name TEXT,
              last_name TEXT,
              age INTEGER,
              phone_number TEXT)''')

conn.close()