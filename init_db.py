import sqlite3

def initialize_database():
    conn = sqlite3.connect('rubber_duck.db')
    cur = conn.cursor()

    results_table_query = """
        CREATE TABLE IF NOT EXISTS
        duck_results (
            id TEXT PRIMARY KEY,
            confidence_score FLOAT NOT NULL,
            s3_key TEXT NOT NULL,
            s3_url TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """

    cur.execute(results_table_query)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    initialize_database()
    print("Database table created!")
