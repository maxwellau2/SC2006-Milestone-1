import sqlite3
import sys
from migration_utils import run_migration


def up():
    conn: sqlite3.Connection = sqlite3.connect("database/rewards.db")
    """Create the Reward table if it doesn't exist."""
    create_table_query = """
    CREATE TABLE IF NOT EXISTS Reward (
        RewardID TEXT PRIMARY KEY,  -- Store UUID as text
        Description TEXT NOT NULL,
        PointsRequired INTEGER NOT NULL CHECK(PointsRequired > 0),  -- Ensure points required is greater than zero
        Validity INTEGER NOT NULL ,
        Availability INTEGER NOT NULL CHECK(Availability >= 0)  -- Ensure availability is non-negative
        );
    """
    try:
        cursor = conn.cursor()
        cursor.execute(create_table_query)
        conn.commit()
        print("Reward table created successfully.")
    except sqlite3.Error as e:
        print(e)
    finally:
        conn.close()


def down():
    conn: sqlite3.Connection = sqlite3.connect("database/rewards.db")

    """Delete the Reward table if it exists."""
    drop_table_query = "DROP TABLE IF EXISTS Reward;"
    try:
        cursor = conn.cursor()
        cursor.execute(drop_table_query)
        conn.commit()
        print("Reward table deleted successfully.")
    except sqlite3.Error as e:
        print(e)
    finally:
        conn.close()


if __name__ == "__main__":
    run_migration(up, down)
