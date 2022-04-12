from copy import error
import sqlite3

def initDB(db_path):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    try:
        cur.execute("""CREATE TABLE IF NOT EXISTS user (
                        sessionId TEXT PRIMARY KEY,
                        id TEXT NOT NULL
                    ); """)

        cur.execute("""CREATE TABLE IF NOT EXISTS action (
                        time DATETIME DEFAULT UTC,
                        user_sessionId TEXT,
                        type TEXT NOT NULL,
                        locationX INTEGER IF NOT NULL,
                        locationY INTEGER IF NOT NULL,
                        viewedId TEXT,
                        pageFrom TEXT,
                        pageTo TEXT,
                        FOREIGN KEY (user_sessionId) REFERENCES user(sessionId)
                    ); """)
        conn.commit()                  
        cur.close()
    except error as e:
        print(e)


