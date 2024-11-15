import pytest
import sqlite3
from src.reports.services.PointsService import PointsService


@pytest.fixture
def db_connection():
    """Creates a new SQLite in-memory database and initializes the required tables for testing."""
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()

    # Create the User table as expected by PointsService
    cursor.execute(
        """
        CREATE TABLE User (
            userID TEXT PRIMARY KEY,
            userName TEXT,
            passwordHash TEXT,
            emailAddress TEXT,
            loginStatus BOOLEAN,
            points INTEGER,
            notificationPreference TEXT,
            notificationEnabled BOOLEAN,
            isAuthority BOOLEAN,
            isModerator BOOLEAN
        );
    """
    )
    conn.commit()
    yield conn
    conn.close()


@pytest.fixture
def points_service(db_connection):
    """Initialize PointsService with the in-memory database."""
    return PointsService(db_connection)


def test_create_user(points_service, db_connection):
    """Test creating a user in the User table."""
    user_id = "test_user_1"
    points_service.create_user(user_id)

    cursor = db_connection.cursor()
    cursor.execute("SELECT * FROM User WHERE userID = ?", (user_id,))
    result = cursor.fetchone()

    assert result is not None
    assert result[0] == user_id
    assert result[5] == 0  # Check initial points set to 0


def test_check_user_exists(points_service):
    """Test checking if a user exists, and creation if not."""
    user_id = "test_user_2"
    exists_before = points_service.check_user_exists(user_id)
    exists_after = points_service.check_user_exists(user_id)

    assert not exists_before  # User didn't exist initially
    assert exists_after  # User should exist after checking


def test_get_point_from_user_id(points_service):
    """Test retrieving points for a user."""
    user_id = "test_user_3"
    points_service.create_user(user_id)

    points = points_service.get_point_from_user_id(user_id)
    assert points == 0  # Initial points should be 0


def test_update_point_for_user_id(points_service, db_connection):
    """Test updating points for a user."""
    user_id = "test_user_4"
    points_service.create_user(user_id)

    # Update points
    new_points = 100
    result_code = points_service.update_point_for_user_id(
        user_id, new_points, "test_report_id"
    )

    # Verify the update
    cursor = db_connection.cursor()
    cursor.execute("SELECT points FROM User WHERE userID = ?", (user_id,))
    updated_points = cursor.fetchone()[0]

    assert result_code == 200
    assert updated_points == new_points
