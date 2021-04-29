import sqlite3

# Run this file to create the datebase

connection = sqlite3.connect('accounts.db')
cursor = connection.cursor()

cursor.execute("""CREATE TABLE accounts (
                 username text,
                 password text,
                 balance float,
                 pin_code int,
                 in_use int
                 )""")

connection.commit()

connection.close()
