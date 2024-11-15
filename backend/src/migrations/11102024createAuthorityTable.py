import sqlite3
import os
from migration_utils import run_migration


def get_connection_instance(
    db_name: str = "database/authority.db",
) -> sqlite3.Connection:
    """Establish a new connection to the database."""
    return sqlite3.connect(db_name)


def up():
    """Create the Authority table if it doesn't exist."""
    conn = get_connection_instance()  # Specify your new DB file here
    create_table_query = """
    CREATE TABLE IF NOT EXISTS Authority (
        UserID TEXT PRIMARY KEY,
        AuthorityName TEXT NOT NULL
    );
    """
    try:
        cursor = conn.cursor()
        cursor.execute(create_table_query)
        conn.commit()
        print("Authority table created successfully in new_database.db.")
    except sqlite3.Error as e:
        print(f"Error creating Authority table: {e}")
    finally:
        conn.close()


def down():
    """Delete the Authority table if it exists."""
    conn = get_connection_instance()
    drop_table_query = "DROP TABLE IF EXISTS Authority;"
    try:
        cursor = conn.cursor()
        cursor.execute(drop_table_query)
        conn.commit()
        print("Authority table deleted successfully from new_database.db.")
    except sqlite3.Error as e:
        print(f"Error deleting Authority table: {e}")
    finally:
        conn.close()


if __name__ == "__main__":
    run_migration(up, down)
