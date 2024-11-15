import sqlite3
from migration_utils import run_migration

DATABASE_PATH = "database/users.db"


def up() -> None:
    conn = sqlite3.connect(DATABASE_PATH)
    try:
        cursor = conn.cursor()

        # Create ResetPassword table
        create_reset_password_table_query = """
        CREATE TABLE IF NOT EXISTS ResetPassword (
            userID TEXT NOT NULL,               -- Reference to user's UUID
            verificationKey TEXT NOT NULL      -- Unique verification key for password reset
        );
        """
        cursor.execute(create_reset_password_table_query)

        conn.commit()
        print("ResetPassword table created successfully.")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()


def down() -> None:
    conn = sqlite3.connect(DATABASE_PATH)
    try:
        cursor = conn.cursor()

        # Drop ResetPassword table
        drop_reset_password_table_query = "DROP TABLE IF EXISTS ResetPassword;"
        cursor.execute(drop_reset_password_table_query)

        conn.commit()
        print("ResetPassword table dropped successfully.")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()


if __name__ == "__main__":
    run_migration(up, down)
