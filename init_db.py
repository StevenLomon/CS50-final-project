import sqlite3

def initialize_database():
    conn = sqlite3.connect('rubber_duck.db')
    cur = conn.cursor()

    results_table_query = """
        CREATE TABLE IF NOT EXISTS
        duck_results (
            id TEXT PRIMARY KEY,
            duck_found BOOLEAN NOT NULL,
            bounding_box_available BOOLEAN NOT NULL,
            confidence_score FLOAT,
            bounding_box_data TEXT,
            s3_key TEXT NOT NULL,
            s3_url TEXT NOT NULL,
            s3_url_bounding_box TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """

    cur.execute(results_table_query)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    initialize_database()
    print("Database table created!")
