import pytest
import sqlite3
from src.reports.services.ReportService import ReportService
from src.reports.models.ReportModels import Report
from datetime import datetime
import uuid


@pytest.fixture
def db_connection():
    """Creates a new SQLite in-memory database and initializes the required tables for testing."""
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()

    # Create the Report table as expected by ReportService
    cursor.execute(
        """
        CREATE TABLE Report (
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
            OllamaDescription TEXT,
            AuthorityID TEXT
        );
    """
    )
    conn.commit()
    yield conn
    conn.close()


@pytest.fixture
def report_service(db_connection):
    """Initialize ReportService with the in-memory database."""
    return ReportService(db_connection)


@pytest.fixture
def sample_report():
    """Provides a sample Report object for testing."""
    return Report(
        user_id="test_user",
        relevance=5,
        severity=7,
        urgency=4,
        status="Pending",
        report_id=str(uuid.uuid4()),
        description="Sample report description",
        image_path="path/to/image.jpg",
        title="Sample Report",
        datetime=int(datetime.now().timestamp()),
        location="Sample Location",
        points=10,
        ollama_description="Sample Ollama Description",
        authority_id="auth_id_1",
    )


def test_create_report(report_service, sample_report, db_connection):
    """Test creating a report in the Report table."""
    status_code, created_report = report_service.create_report(sample_report)
    assert status_code == 201
    assert created_report.report_id == sample_report.report_id

    # Verify that the report was actually inserted
    cursor = db_connection.cursor()
    cursor.execute(
        "SELECT * FROM Report WHERE ReportID = ?", (sample_report.report_id,)
    )
    result = cursor.fetchone()
    assert result is not None


def test_check_report_exists(report_service, sample_report):
    """Test checking if a report exists in the Report table."""
    report_service.create_report(sample_report)
    exists = report_service.check_report_exists(sample_report.report_id)
    assert exists is True

    # Test for a non-existent report
    non_existent_id = str(uuid.uuid4())
    exists = report_service.check_report_exists(non_existent_id)
    assert exists is False


def test_update_report_status(report_service, sample_report):
    """Test updating the status of a report."""
    report_service.create_report(sample_report)

    # Update status
    new_status = "In Progress"
    result_code = report_service.update_report_status(
        sample_report.report_id, new_status
    )
    assert result_code == 200

    # Verify the status update
    cursor = report_service.conn.cursor()
    cursor.execute(
        "SELECT Status FROM Report WHERE ReportID = ?", (sample_report.report_id,)
    )
    result = cursor.fetchone()
    assert result[0] == new_status


def test_read_report_by_id(report_service, sample_report):
    """Test fetching a report by ReportID."""
    report_service.create_report(sample_report)

    # Fetch the report
    status_code, report = report_service.read_report_by_id(sample_report.report_id)
    assert status_code == 200
    assert report.report_id == sample_report.report_id


def test_delete_report_by_id(report_service, sample_report):
    """Test deleting a report by ReportID."""
    report_service.create_report(sample_report)

    # Delete the report
    result_code = report_service.delete_report_by_id(sample_report.report_id)
    assert result_code == 200

    # Verify deletion
    exists = report_service.check_report_exists(sample_report.report_id)
    assert exists is False


def test_get_top_k_reports_by_severity(report_service, sample_report, db_connection):
    """Test fetching top k reports by severity."""
    # Insert multiple reports with varying severity
    for i in range(5):
        report = Report(
            user_id="test_user",
            relevance=5,
            severity=10 - i,  # Decreasing severity
            urgency=4,
            status="Pending",
            report_id=str(uuid.uuid4()),
            description=f"Report {i}",
            image_path="path/to/image.jpg",
            title=f"Report {i}",
            datetime=int(datetime.now().timestamp()),
            location="Sample Location",
            points=10,
            ollama_description="Sample Ollama Description",
            authority_id="auth_id_1",
        )
        report_service.create_report(report)

    # Fetch top 3 reports by severity
    status_code, top_reports = report_service.get_top_k_reports_by_severity(3)
    assert status_code == 200
    assert len(top_reports) == 3
    assert top_reports[0].severity > top_reports[1].severity >= top_reports[2].severity


def test_search_reports_by_description(report_service, sample_report, db_connection):
    """Test searching reports by description."""
    report_service.create_report(sample_report)

    # Search for the report by description keyword
    status_code, reports = report_service.search_reports_by_description("sample")
    assert status_code == 200
    assert len(reports) > 0
    assert any("sample" in report.description.lower() for report in reports)


def test_update_report_points(report_service, sample_report):
    """Test updating points for a report."""
    report_service.create_report(sample_report)

    # Update points
    new_points = 50
    result_code = report_service.update_report_points(
        sample_report.report_id, new_points
    )
    assert result_code == 200

    # Verify the points update
    cursor = report_service.conn.cursor()
    cursor.execute(
        "SELECT Points FROM Report WHERE ReportID = ?", (sample_report.report_id,)
    )
    updated_points = cursor.fetchone()[0]
    assert updated_points == new_points
