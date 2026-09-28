import sqlite3


def build_database(races_df, events_df, results_df, db_path):
    """
    Build a SQLite database from cleaned 5k datasets.

    Args:
        races_df (pandas.DataFrame): Race metadata
        events_df (pandas.DataFrame): Event- metadata
        results_df (pandas.DataFrame): Cleaned participant results
        db_path (str): Path where the SQLite database will be created

    Returns:
        sqlite3.Connection: Open connection to the database
    """
    sql_results_df = results_df[[
        "result_id", 
        "event_id", 
        "place", 
        "gender", 
        "age", 
        "chip_time_seconds",
        "pace", 
        "age_percentage_numeric"
    ]].copy()

    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.execute("DROP TABLE IF EXISTS results;")
    conn.execute("DROP TABLE IF EXISTS events;")
    conn.execute("DROP TABLE IF EXISTS races;")
    conn.execute("""
        CREATE TABLE races (
            race_id INTEGER PRIMARY KEY,
            race_name TEXT NOT NULL,
            city TEXT,
            state TEXT,
            country_code TEXT,
            timezone TEXT
        );
    """)
    conn.execute("""
        CREATE TABLE events (
            event_id INTEGER PRIMARY KEY,
            race_id INTEGER NOT NULL,
            event_name TEXT NOT NULL,
            event_date TEXT NOT NULL,
            distance_km REAL NOT NULL,
            FOREIGN KEY (race_id) REFERENCES races(race_id)
        );
    """)
    conn.execute("""
        CREATE TABLE results (
            result_id INTEGER PRIMARY KEY,
            event_id INTEGER NOT NULL,
            place INTEGER,
            gender TEXT NOT NULL,
            age INTEGER,
            chip_time_seconds REAL,
            pace TEXT,
            age_percentage_numeric REAL,
            FOREIGN KEY (event_id) REFERENCES events(event_id)
        );  
    """)

    races_df.to_sql("races", conn, if_exists="append", index=False)
    events_df.to_sql("events", conn, if_exists="append", index=False)
    sql_results_df.to_sql("results", conn, if_exists="append",
                           index=False)
    
    return conn