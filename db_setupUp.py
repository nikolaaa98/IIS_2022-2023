import sqlite3


connection = sqlite3.connect("training_data.db")
cursor = connection.cursor()

command1 = """CREATE TABLE IF NOT EXISTS
stores(store_id INTEGER PRIMARY KEY, location TEXT)"""

cursor.execute(command1)

cursor.execute("INSERT INTO stores VALUES (21, 'Mineapolis, MN')")
cursor.execute("INSERT INTO stores VALUES (95, 'Chicago, IL')")
cursor.execute("INSERT INTO stores VALUES (64, 'Iowa City, IA')")

cursor.execute("SELECT * from stores")
result = cursor.fetchall()
print(result)