import sqlite3
import sys
from migration_utils import run_migration


def up():
    conn: sqlite3.Connection = sqlite3.connect("database/points.db")
    """Create the Points table if it doesn't exist."""
    create_table_query = """
    CREATE TABLE IF NOT EXISTS Points (
        UserID TEXT NOT NULL,  -- Store UUID as text
        Points INTEGER NOT NULL,
        LastUpdated INTEGER NOT NULL,
        PRIMARY KEY (UserID)
    );
    """
    try:
        cursor = conn.cursor()
        cursor.execute(create_table_query)
        conn.commit()
        print("Points table created successfully.")
    except sqlite3.Error as e:
        print(e)
    finally:
        conn.close()


def down():
    conn: sqlite3.Connection = sqlite3.connect("database/points.db")

    """Delete the Points table if it exists."""
    drop_table_query = "DROP TABLE IF EXISTS points;"
    try:
        cursor = conn.cursor()
        cursor.execute(drop_table_query)
        conn.commit()
        print("Points table deleted successfully.")
    except sqlite3.Error as e:
        print(e)
    finally:
        conn.close()


if __name__ == "__main__":
    run_migration(up, down)
