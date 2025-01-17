import sqlite3

def init_db(conn: sqlite3.Connection):
    c = conn.cursor()
    
    c.execute("""
        CREATE TABLE IF NOT EXISTS teams (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE
        )
    """)
    
    c.execute("""
        CREATE TABLE IF NOT EXISTS members (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            team_id INTEGER,
            name TEXT,
            FOREIGN KEY (team_id) REFERENCES teams (id)
        )
    """)
    
    c.execute("""
        CREATE TABLE IF NOT EXISTS exercises (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            points_per_rep INTEGER
        )
    """)
    
    c.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            team_id INTEGER,
            member_id INTEGER,
            exercise_id INTEGER,
            reps INTEGER,
            points INTEGER,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (team_id) REFERENCES teams (id),
            FOREIGN KEY (member_id) REFERENCES members (id),
            FOREIGN KEY (exercise_id) REFERENCES exercises (id)
        )
    """)
    
    conn.commit()

def get_conn():
    return sqlite3.connect("exercise_tracker.db")
