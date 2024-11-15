import sqlite3
from typing import List, Tuple, Optional
from src.reports.models.ReportModels import (
    Report,
)  # Assuming the Report model is stored here
from src.users.services.UserService import UserService


class ReportService:
    def __init__(self, conn: sqlite3.Connection):
        """Initialize the ReportService with a connection to the SQLite database."""
        self.conn = conn

    def create_report_table(self):
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
            Title TEXT,
            Datetime INTEGER NOT NULL,
            Location TEXT NOT NULL,
            Points INTEGER DEFAULT 0,
            OllamaDescription TEXT
        );
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute(create_table_query)
            self.conn.commit()
            print("Report table created successfully.")
        except sqlite3.Error as e:
            print(f"Error creating table: {e}")

    def create_report(self, report: Report) -> Tuple[int, Optional[Report]]:
        """Insert a new report into the Report table."""
        insert_query = """
        INSERT INTO Report (UserID, Relevance, Severity, Urgency, Status, ReportID, Description, imagePath, Title, Datetime, Location, Points, OllamaDescription, AuthorityID)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                insert_query,
                (
                    report.user_id,
                    report.relevance,
                    report.severity,
                    report.urgency,
                    report.status,
                    report.report_id,
                    report.description,
                    report.image_path,
                    report.title,
                    report.datetime,
                    report.location,
                    report.points,
                    report.ollama_description,
                    report.authority_id,
                ),
            )
            self.conn.commit()
            return 201, report  # Created
        except sqlite3.IntegrityError as e:
            print(e)
            return 400, None  # Bad request: report_id already exists
        except sqlite3.Error as e:
            print(f"Error inserting report: {e}")
            return 500, None  # Internal server error

    def check_report_exists(self, report_id: str) -> bool:
        """Check if a report exists in the Report table. Create the report if they do not exist."""
        query = "SELECT * FROM Report WHERE ReportID = ?;"
        cursor = self.conn.cursor()
        cursor.execute(query, (report_id,))
        result = cursor.fetchone()
        if result:
            return True
        else:
            return False

    def read_report_by_authority_id(
        self, authority_id: str
    ) -> Tuple[int, List[Report]]:
        """Fetch all reports from the Report table by authority ID."""
        print(authority_id)
        query = "SELECT * FROM Report WHERE AuthorityID = ? ORDER BY datetime DESC"
        cursor = self.conn.cursor()
        cursor.execute(query, (authority_id,))
        results = cursor.fetchall()
        reports = [Report(**self._parse_report(result)) for result in results]
        return 200, reports  # OK

    def update_report_status(self, report_id: str, status: str) -> int:
        """Update the status of a report in the Report table."""
        # check if report exists
        if not self.check_report_exists(report_id):
            return 404  # Not Found
        query = "UPDATE Report SET Status = ? WHERE ReportID = ?;"
        cursor = self.conn.cursor()
        cursor.execute(query, (status, report_id))
        self.conn.commit()
        if cursor.rowcount == 0:
            return 404  # Not Found
        return 200  # OK

    def read_report_by_user_id(self, user_id: str) -> Tuple[int, List[Report]]:
        """Fetch all reports from the Report table by user ID."""
        # check if user exists
        if not self.check_user_exists(user_id):
            return 404, {"detail": "User not found"}
        query = "SELECT * FROM Report WHERE UserID = ? ORDER BY datetime DESC"
        cursor = self.conn.cursor()
        cursor.execute(query, (user_id,))
        results = cursor.fetchall()
        reports = [Report(**self._parse_report(result)) for result in results]
        return 200, reports  # OK

    def get_top_k_reports_by_severity(
        self, k: int, resolved: bool = False
    ) -> Tuple[int, List[Report]]:
        """Fetch top k reports from the Report table by severity."""
        query = "SELECT * FROM Report ORDER BY Severity DESC LIMIT ?"
        if not resolved:
            query = "SELECT * FROM Report WHERE Status = 'Pending' ORDER BY Severity DESC LIMIT ?"
        cursor = self.conn.cursor()
        cursor.execute(query, (k,))
        results = cursor.fetchall()
        reports = [Report(**self._parse_report(result)) for result in results]
        return 200, reports  # OK

    def read_report_by_id(self, report_id: str) -> Tuple[int, Optional[Report]]:
        """Fetch a report by ReportID."""
        # check if user exists
        query = "SELECT * FROM Report WHERE ReportID = ?"
        cursor = self.conn.cursor()
        cursor.execute(query, (report_id,))
        result = cursor.fetchone()
        if result:
            return 200, Report(**self._parse_report(result))  # OK
        else:
            return 404, None  # Not Found

    def search_reports_by_description(
        self, description: str
    ) -> Tuple[int, List[Report]]:
        """Search reports by description using wildcards."""
        query = "SELECT * FROM Report WHERE Description LIKE ?"
        wildcard_description = f"%{description}%"
        cursor = self.conn.cursor()
        cursor.execute(query, (wildcard_description,))
        results = cursor.fetchall()
        reports = [Report(**self._parse_report(result)) for result in results]
        return 200, reports  # OK

    def search_reports_by_title(self, title: str) -> Tuple[int, List[Report]]:
        """Search reports by title using wildcards."""
        query = "SELECT * FROM Report WHERE Title LIKE ?"
        wildcard_title = f"%{title}%"
        cursor = self.conn.cursor()
        cursor.execute(query, (wildcard_title,))
        results = cursor.fetchall()
        reports = [Report(**self._parse_report(result)) for result in results]
        return 200, reports  # OK

    def delete_report_by_id(self, report_id: str) -> int:
        """Delete a report from the Report table by ReportID."""
        delete_query = "DELETE FROM Report WHERE ReportID = ?"
        cursor = self.conn.cursor()
        cursor.execute(delete_query, (report_id,))
        self.conn.commit()
        if cursor.rowcount == 0:
            return 404  # Not Found
        return 200  # OK

    def update_report_points(self, report_id: str, points: int) -> int:
        """Update the points of a report in the database."""
        update_query = "UPDATE Report SET Points = ? WHERE ReportID = ?"
        cursor = self.conn.cursor()
        cursor.execute(update_query, (points, report_id))
        self.conn.commit()
        return 200

    def _parse_report(self, result: Tuple) -> dict:
        """Helper method to parse a database row into a Report dictionary."""
        return {
            "user_id": result[0],
            "relevance": result[1],
            "severity": result[2],
            "urgency": result[3],
            "status": result[4],
            "report_id": result[5],
            "description": result[6],
            "image_path": result[7],
            "title": result[8],
            "datetime": result[9],
            "location": result[10],
            "points": result[11],
            "ollama_description": result[12],
            "authority_id": result[13],
        }

    def close_connection(self):
        """Close the database connection."""
        if self.conn:
            self.conn.close()
            print("Database connection closed.")

    def check_user_exists(self, user_id: str) -> bool:
        """Check if a user exists in the database using UserService."""
        return UserService(sqlite3.connect("database/users.db")).check_user_exists(
            user_id
        )
