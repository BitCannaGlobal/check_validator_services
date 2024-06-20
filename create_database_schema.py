import sqlite3
from contextlib import closing

database = 'VIP.db'


with closing(sqlite3.connect(database)) as connection:
    with closing(connection.cursor()) as cursor:
        cursor.execute("CREATE TABLE services (service TEXT, result TEXT, owner TEXT, url TEXT, extra_output TEXT, current_date TEXT)")
        rows = cursor.execute("SELECT * FROM services").fetchall()
        print(rows)


#### More useful queries:
        
# TRUNCATE TABLE services
# cursor.execute("ALTER TABLE services ADD date datetime;")
# cursor.execute("CREATE TABLE services (service TEXT, result TEXT, owner TEXT, url TEXT, extra_output TEXT)")
# cursor.execute("DELETE FROM services;")
