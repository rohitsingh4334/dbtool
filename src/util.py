import sqlite3

def get_conn(db_name):
    conn = None
    try:
        conn = sqlite3.connect(db_name)
    except (sqlite3.DatabaseError, sqlite3.Error, ValueError) as e:
        print("Error: %s" % e)
        if conn:
            conn.close()
    return conn
