import pytest
import sqlite3
import uuid
from src.users.services.UserService import UserService
from src.users.models.UserModels import User, UserRead, UserUpdate


@pytest.fixture
def db_connection():
    """Creates a new SQLite in-memory database and initializes the required tables for testing."""
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()

    # Create the User table as expected by UserService
    cursor.execute(
        """
        CREATE TABLE User (
            userID TEXT PRIMARY KEY,
            userName TEXT NOT NULL,
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
    )
    conn.commit()
    yield conn
    conn.close()


@pytest.fixture
def user_service(db_connection):
    """Initialize UserService with the in-memory database."""
    return UserService(db_connection)


@pytest.fixture
def sample_user():
    """Provides a sample User object for testing."""
    return User(
        userID=str(uuid.uuid4()),
        userName="testuser",
        passwordHash="hashed_password",
        emailAddress="testuser@example.com",
        loginStatus=False,
        points=100,
        notificationPreference="email",
        notificationEnabled=True,
        isAuthority=False,
        isModerator=False,
    )


def test_create_user(user_service, sample_user, db_connection):
    """Test creating a user in the User table."""
    status_code, created_user = user_service.create_user(sample_user)
    assert status_code == 201
    assert str(created_user.userID) == sample_user.userID

    # Verify that the user was actually inserted
    cursor = db_connection.cursor()
    cursor.execute("SELECT * FROM User WHERE userID = ?", (sample_user.userID,))
    result = cursor.fetchone()
    assert result is not None


def test_read_all_users(user_service, sample_user):
    """Test retrieving all users from the User table."""
    user_service.create_user(sample_user)
    status_code, users = user_service.read_all_users()
    assert status_code == 200
    assert len(users) == 1
    assert users[0].userID == uuid.UUID(sample_user.userID)


def test_check_user_exists(user_service, sample_user):
    """Test checking if a user exists in the User table."""
    user_service.create_user(sample_user)
    exists = user_service.check_user_exists(sample_user.userID)
    assert exists is True

    # Test for a non-existent user
    non_existent_id = str(uuid.uuid4())
    exists = user_service.check_user_exists(non_existent_id)
    assert exists is False


def test_read_user(user_service, sample_user):
    """Test retrieving a user by userID."""
    user_service.create_user(sample_user)

    # Retrieve the user
    status_code, user = user_service.read_user(uuid.UUID(sample_user.userID))
    assert status_code == 200
    assert user.userID == uuid.UUID(sample_user.userID)

    # Test non-existent user retrieval
    non_existent_id = str(uuid.uuid4())
    status_code, user = user_service.read_user(uuid.UUID(non_existent_id))
    assert status_code == 404
    assert user is None


def test_update_user_points(user_service, sample_user):
    """Test updating a user's points."""
    user_service.create_user(sample_user)

    # Update points
    new_points = 200
    result_code = user_service.update_user_points(
        uuid.UUID(sample_user.userID), new_points
    )
    assert result_code == 200

    # Verify the points update
    cursor = user_service.conn.cursor()
    cursor.execute("SELECT points FROM User WHERE userID = ?", (sample_user.userID,))
    updated_points = cursor.fetchone()[0]
    assert updated_points == new_points


def test_update_user(user_service, sample_user):
    """Test updating a user's details."""
    user_service.create_user(sample_user)

    # Prepare updated data
    user_update = UserUpdate(
        userName="updateduser", emailAddress="updateduser@example.com"
    )

    # Update the user
    result_code = user_service.update_user(uuid.UUID(sample_user.userID), user_update)
    assert result_code == 200

    # Verify the update
    cursor = user_service.conn.cursor()
    cursor.execute(
        "SELECT userName, emailAddress FROM User WHERE userID = ?",
        (sample_user.userID,),
    )
    result = cursor.fetchone()
    assert result == (user_update.userName, user_update.emailAddress)


def test_delete_user(user_service, sample_user):
    """Test deleting a user by userID."""
    user_service.create_user(sample_user)

    # Delete the user
    result_code = user_service.delete_user(uuid.UUID(sample_user.userID))
    assert result_code == 200

    # Verify deletion
    exists = user_service.check_user_exists(sample_user.userID)
    assert exists is False


def test_wipe_clean(user_service, sample_user, db_connection):
    """Test deleting all users from the User table."""
    user_service.create_user(sample_user)

    # Wipe all users
    result_code = user_service.wipeClean()
    assert result_code == 200

    # Verify the table is empty
    cursor = db_connection.cursor()
    cursor.execute("SELECT * FROM User;")
    results = cursor.fetchall()
    assert len(results) == 0
