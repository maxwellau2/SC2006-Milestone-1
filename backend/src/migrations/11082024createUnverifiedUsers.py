import sqlite3
from migration_utils import run_migration

DATABASE_PATH = "database/users.db"


def up() -> None:
    conn = sqlite3.connect(DATABASE_PATH)
    try:
        cursor = conn.cursor()

        # Create UnverifiedUser table
        create_unverified_user_table_query = """
        CREATE TABLE IF NOT EXISTS UnverifiedUser (
            userID TEXT PRIMARY KEY,          -- Store UUID as text
            userName TEXT NOT NULL UNIQUE,    -- Unique username
            passwordHash TEXT NOT NULL,
            emailAddress TEXT NOT NULL UNIQUE, -- Unique email
            loginStatus BOOLEAN NOT NULL,
            points INTEGER NOT NULL,
            notificationPreference TEXT CHECK(notificationPreference IN ('email', 'sms', 'push')),
            notificationEnabled BOOLEAN NOT NULL,
            isAuthority BOOLEAN NOT NULL,
            isModerator BOOLEAN NOT NULL,
            verificationKey TEXT NOT NULL      -- Unique verification key
        );
        """
        cursor.execute(create_unverified_user_table_query)

        conn.commit()
        print("Tables created successfully.")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()


def down() -> None:
    conn = sqlite3.connect(DATABASE_PATH)
    try:
        cursor = conn.cursor()

        # Drop UnverifiedUser table
        drop_unverified_user_table_query = "DROP TABLE IF EXISTS UnverifiedUser;"
        cursor.execute(drop_unverified_user_table_query)

        conn.commit()
        print("Tables dropped successfully.")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()


if __name__ == "__main__":
    run_migration(up, down)
