import sqlite3
import datetime
from math import sqrt
import re

def check_formatting_float(value):
    try:
        float_value = float(value)
        if float_value < 0:
            print("enter a positive value")
        elif float_value > 1e6:
            print("This value seems to big. Enter a value less than 1,000,000")
        else:
            print("Test OK!")
            loop = False
    except:
        print("please enter a valid float")

def check_formatting_date(date):
    regex = r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}(.\d+)?"
    if re.match(regex, date):
        return True
    else:
        return False

date = "2023-10-15 16:39:29.205804"
print(check_formatting_date(date))

quit()

conn = sqlite3.connect("history.db")
print("opened db successfully")

request =\
'''
    CREATE TABLE IF NOT EXISTS history(id INT, weight DECIMAL(10,3), TakeOffDist DECIMAL(10,3),
    weightDestroyed DECIMAL(10,3), time DATETIME);
'''
conn.execute(request)
conn.commit()
print("Table created successfully")

def write_input(weight, TakeOffDist, weightDestroyed, time):
    # Find new ID:
    query = "SELECT MAX(id) FROM history"
    res = conn.execute(query)
    id = res.fetchall()[0][0]+1

    conn.execute(f"INSERT INTO history VALUES({id}, {weight}, {TakeOffDist}, {weightDestroyed}, {time})")
    conn.commit()
    print("Data inserted successfully")


write_input(0, 0, 0, 0)

print("Done")
