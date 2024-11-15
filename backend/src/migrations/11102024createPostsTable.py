import sqlite3
from migration_utils import run_migration


def get_connection_instance(db_name: str = "database/posts.db") -> sqlite3.Connection:
    """Establish a new connection to the database."""
    return sqlite3.connect(db_name)


def up():
    """Create the Post table if it doesn't exist."""
    conn = get_connection_instance()  # Specify your new DB file here
    create_table_query = """
    CREATE TABLE IF NOT EXISTS Post (
        PostID TEXT PRIMARY KEY,
        Title TEXT,
        Description TEXT,
        imagePath TEXT,
        AuthorityName TEXT NOT NULL,
        UserName TEXT,
        UserID TEXT,
        time INTEGER NOT NULL
    );
    """
    try:
        cursor = conn.cursor()
        cursor.execute(create_table_query)
        conn.commit()
        print("Post table created successfully in posts.db.")
    except sqlite3.Error as e:
        print(f"Error creating Post table: {e}")
    finally:
        conn.close()


def down():
    """Delete the Post table if it exists."""
    conn = get_connection_instance()
    drop_table_query = "DROP TABLE IF EXISTS Post;"
    try:
        cursor = conn.cursor()
        cursor.execute(drop_table_query)
        conn.commit()
        print("Post table deleted successfully from posts.db.")
    except sqlite3.Error as e:
        print(f"Error deleting Post table: {e}")
    finally:
        conn.close()


if __name__ == "__main__":
    run_migration(up, down)
