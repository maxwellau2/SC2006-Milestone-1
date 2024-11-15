import sqlite3
from typing import Optional, Tuple, List
from src.posts.models.AuthorityModel import (
    Authority,
)  # Assuming the Authority model is stored in this location


class AuthorityService:
    @staticmethod
    def get_connection_instance() -> sqlite3.Connection:
        """Establish a new connection to the database."""
        return sqlite3.connect("database/authority.db")

    @staticmethod
    def create_authority_table():
        """Create the Authority table if it doesn't exist."""
        conn = AuthorityService.get_connection_instance()
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
            print("Authority table created successfully.")
        except sqlite3.Error as e:
            print(f"Error creating Authority table: {e}")
        finally:
            conn.close()

    #
    @staticmethod
    def create_entry(authority: Authority) -> Tuple[int, Optional[Authority]]:
        """Insert a new authority into the Authority table."""
        conn = AuthorityService.get_connection_instance()
        insert_query = """
        INSERT INTO Authority (UserID, AuthorityName)
        VALUES (?, ?);
        """
        try:
            cursor = conn.cursor()
            cursor.execute(insert_query, (authority.user_id, authority.authority_name))
            conn.commit()
            return 201, authority  # Created
        except sqlite3.IntegrityError as e:
            print(e)
            return 400, None  # Bad request: user_id already exists
        except sqlite3.Error as e:
            print(f"Error inserting authority: {e}")
            return 500, None  # Internal server error
        finally:
            conn.close()

    @staticmethod
    def update_entry(user_id: str, new_authority_name: str) -> int:
        """Update the authority name for an existing authority."""
        conn = AuthorityService.get_connection_instance()
        update_query = """
        UPDATE Authority SET AuthorityName = ? WHERE UserID = ?;
        """
        try:
            cursor = conn.cursor()
            cursor.execute(update_query, (new_authority_name, user_id))
            conn.commit()
            if cursor.rowcount == 0:
                return 404  # Not Found
            return 200  # OK
        except sqlite3.Error as e:
            print(f"Error updating authority: {e}")
            return 500  # Internal server error
        finally:
            conn.close()

    @staticmethod
    def delete_entry(user_id: str) -> int:
        """Delete an authority from the Authority table by user ID."""
        conn = AuthorityService.get_connection_instance()
        delete_query = "DELETE FROM Authority WHERE UserID = ?;"
        try:
            cursor = conn.cursor()
            cursor.execute(delete_query, (user_id,))
            conn.commit()
            if cursor.rowcount == 0:
                return 404  # Not Found
            return 200  # OK
        except sqlite3.Error as e:
            print(f"Error deleting authority: {e}")
            return 500  # Internal server error
        finally:
            conn.close()

    @staticmethod
    def read_entry(user_id: str) -> Tuple[int, Optional[Authority]]:
        """Fetch an authority by user ID."""
        conn = AuthorityService.get_connection_instance()
        query = "SELECT * FROM Authority WHERE UserID = ?;"
        try:
            cursor = conn.cursor()
            cursor.execute(query, (user_id,))
            result = cursor.fetchone()
            if result:
                authority = AuthorityService.parse_entry(result)
                return 200, authority  # OK
            else:
                return 404, None  # Not Found
        except sqlite3.Error as e:
            print(f"Error reading authority: {e}")
            return 500, None  # Internal server error
        finally:
            conn.close()

    @staticmethod
    def read_all_entries() -> Tuple[int, List[Authority]]:
        """Fetch all authorities from the Authority table."""
        conn = AuthorityService.get_connection_instance()
        query = "SELECT * FROM Authority;"
        try:
            cursor = conn.cursor()
            cursor.execute(query)
            results = cursor.fetchall()
            authorities = [AuthorityService.parse_entry(row) for row in results]
            return 200, authorities  # OK
        except sqlite3.Error as e:
            print(f"Error reading all authorities: {e}")
            return 500, []  # Internal server error
        finally:
            conn.close()

    @staticmethod
    def parse_entry(result: Tuple) -> Authority:
        """Convert a database row into an Authority instance."""
        return Authority(user_id=result[0], authority_name=result[1])
