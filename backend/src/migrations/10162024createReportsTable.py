import sqlite3
import sys
from migration_utils import run_migration


def up():
    conn: sqlite3.Connection = sqlite3.connect("database/reports.db")
    """Create the Report table if it doesn't exist."""
    create_table_query = """
    CREATE TABLE IF NOT EXISTS Report (
        UserID TEXT NOT NULL,
        Relevance INTEGER NOT NULL,
        Severity INTEGER NOT NULL,
        Urgency INTEGER NOT NULL,
        Status TEXT CHECK(Status IN ('Pending', 'In Progress', 'Resolved')) DEFAULT 'Pending',
        ReportID TEXT PRIMARY KEY,
        Description TEXT,
        imagePath TEXT,
        title TEXT,
        Datetime INTEGER NOT NULL,
        Location TEXT NOT NULL,
        Points INTEGER NOT NULL,
        OllamaDescription TEXT,
        AuthorityID TEXT
    );
    """
    try:
        cursor = conn.cursor()
        cursor.execute(create_table_query)
        conn.commit()
        print("Report table created successfully.")
    except sqlite3.Error as e:
        print(f"Error creating Report table: {e}")
    finally:
        conn.close()


def down():
    conn: sqlite3.Connection = sqlite3.connect("database/reports.db")
    """Delete the Report table if it exists."""
    drop_table_query = "DROP TABLE IF EXISTS Report;"
    try:
        cursor = conn.cursor()
        cursor.execute(drop_table_query)
        conn.commit()
        print("Report table deleted successfully.")
    except sqlite3.Error as e:
        print(f"Error deleting Report table: {e}")
    finally:
        conn.close()


if __name__ == "__main__":
    run_migration(up, down)
