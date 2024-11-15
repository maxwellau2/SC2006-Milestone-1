import sqlite3
import sys
from migration_utils import run_migration


def up() -> None:
    conn: sqlite3.Connection = sqlite3.connect("database/users.db")
    """Create the User table if it doesn't exist."""
    create_table_query = """
    CREATE TABLE IF NOT EXISTS User (
        userID TEXT PRIMARY KEY,  -- Store UUID as text
        UserName TEXT NOT NULL,
        passwordHash TEXT NOT NULL,
        emailAddress TEXT NOT NULL,
        loginStatus BOOLEAN NOT NULL,
        points INTEGER NOT NULL,
        notificationPreference TEXT CHECK(notificationPreference IN ('email', 'sms', 'push')),
        notificationEnabled BOOLEAN NOT NULL,
        isAuthority BOOLEAN NOT NULL,
        isModerator BOOLEAN NOT NULL
    );
    """
    try:
        cursor = conn.cursor()
        cursor.execute(create_table_query)
        conn.commit()
        print("User table created successfully.")
    except sqlite3.Error as e:
        print(e)
    finally:
        conn.close()


def down() -> None:
    conn: sqlite3.Connection = sqlite3.connect("database/users.db")
    """Delete the User table if it exists."""
    drop_table_query = "DROP TABLE IF EXISTS User;"
    try:
        cursor = conn.cursor()
        cursor.execute(drop_table_query)
        conn.commit()
        print("User table deleted successfully.")
    except sqlite3.Error as e:
        print(e)
    finally:
        conn.close()


if __name__ == "__main__":
    run_migration(up, down)
