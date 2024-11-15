# migration_utils.py
import sqlite3
import sys


def get_connection(db_path="database/users.db"):
    """Establish a connection to the database."""
    return sqlite3.connect(db_path)


def run_migration(migration_up, migration_down):
    """Run the appropriate migration function based on the command-line argument."""
    # conn = get_connection()
    if len(sys.argv) > 1 and sys.argv[1] == "up":
        migration_up()
    elif len(sys.argv) > 1 and sys.argv[1] == "down":
        migration_down()
    else:
        print("Invalid command line argument.")


if __name__ == "__main__":
    pass
