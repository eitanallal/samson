import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()


cur.execute("INSERT INTO history (id, LoadWeight, WeightDestroyed, TakeOffDistance) VALUES (?, ?, ?, ?)",
            (1, 123, 456, 789)
            )

cur.execute("INSERT INTO history (LoadWeight, WeightDestroyed, TakeOffDistance) VALUES (?, ?, ?)",
            (123, 456, 789)
            )

connection.commit()
connection.close()