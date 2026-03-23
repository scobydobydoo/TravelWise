import sqlite3
def init_db():
    conn=sqlite3.connect("travel.db")
    cur = conn.cursor()
    
    cur.execute(
    """CREATE TABLE IF NOT EXISTS Users(
        id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE,
        password TEXT)
    """    )
    conn.commit()
    conn.close()
init_db()