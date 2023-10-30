import sqlite3
import numpy as np
import pandas as pd

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

'''
<td>{{ line['id'] }}</td>
<td>{{ line['LoadWeight'] }}</td>
<td>{{ line['WeightDestroyed'] }}</td>
<td>{{ line['TakeOffDistance'] }}</td>
<td>{{ line['created_time'] }}</td>

'''
def index():
    conn = get_db_connection()
    history = np.array(conn.execute('SELECT * FROM history').fetchall())
        
    df = pd.DataFrame(history, columns=['id', 'LoadWeight', 'WeightDestroyed', 'TakeOffDistance', 'created_time'])
    df['date'], df['time'] = df['created_time'].str.split(' ', 1).str
    df.drop(columns=['created_time'], inplace=True)
    print (df)
    conn.close()

index()