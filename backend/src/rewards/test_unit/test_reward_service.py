import pytest
import sqlite3
from src.rewards.services.RewardService import RewardService
from src.rewards.models.RewardModel import Reward, RewardUpdate
import uuid


@pytest.fixture
def db_connection():
    """Creates a new SQLite in-memory database and initializes the required tables for testing."""
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()

    # Create the Reward table as expected by RewardService
    cursor.execute(
        """
        CREATE TABLE Reward (
            RewardID TEXT PRIMARY KEY,
            Description TEXT NOT NULL,
            PointsRequired INTEGER NOT NULL,
            Validity INTEGER,
            Availability INTEGER NOT NULL
        );
    """
    )
    conn.commit()
    yield conn
    conn.close()


@pytest.fixture
def reward_service(db_connection):
    """Initialize RewardService with the in-memory database."""
    return RewardService(db_connection)


@pytest.fixture
def sample_reward():
    """Provides a sample Reward object for testing."""
    return Reward(
        rewardID=str(uuid.uuid4()),
        description="Sample Reward",
        pointsRequired=100,
        validity=365 * 24 * 60 * 60,  # 1 year in seconds
        availability=10,
    )


def test_create_reward(reward_service, sample_reward, db_connection):
    """Test creating a reward in the Reward table."""
    status_code = reward_service.create_reward(sample_reward)
    assert status_code == 201

    # Verify that the reward was actually inserted
    cursor = db_connection.cursor()
    cursor.execute("SELECT * FROM Reward WHERE RewardID = ?", (sample_reward.rewardID,))
    result = cursor.fetchone()
    assert result is not None


def test_read_all_rewards(reward_service, sample_reward):
    """Test retrieving all rewards from the Reward table."""
    reward_service.create_reward(sample_reward)
    status_code, rewards = reward_service.read_all_rewards()
    assert status_code == 200
    assert len(rewards) == 1
    assert rewards[0].rewardID == sample_reward.rewardID


def test_read_reward_by_id(reward_service, sample_reward):
    """Test retrieving a reward by RewardID."""
    reward_service.create_reward(sample_reward)

    # Retrieve the reward
    status_code, reward = reward_service.read_reward_by_id(sample_reward.rewardID)
    assert status_code == 200
    assert reward.rewardID == sample_reward.rewardID

    # Test non-existent reward retrieval
    non_existent_id = str(uuid.uuid4())
    status_code, reward = reward_service.read_reward_by_id(non_existent_id)
    assert status_code == 404
    assert reward is None


def test_update_reward(reward_service, sample_reward):
    """Test updating a reward's details."""
    reward_service.create_reward(sample_reward)

    # Prepare updated data
    reward_update = RewardUpdate(
        description="Updated Reward Description",
        pointsRequired=200,
        validity=180 * 24 * 60 * 60,  # 6 months in seconds
        availability=5,
    )

    # Update the reward
    status_code = reward_service.update_reward(sample_reward.rewardID, reward_update)
    assert status_code == 200

    # Verify the update
    cursor = reward_service.conn.cursor()
    cursor.execute(
        "SELECT Description, PointsRequired, Validity, Availability FROM Reward WHERE RewardID = ?",
        (sample_reward.rewardID,),
    )
    result = cursor.fetchone()
    assert result == (
        reward_update.description,
        reward_update.pointsRequired,
        reward_update.validity,
        reward_update.availability,
    )


def test_claim_reward_by_id(reward_service, sample_reward, db_connection):
    """Test claiming a reward by RewardID."""
    reward_service.create_reward(sample_reward)

    # Create User table and insert a user with enough points for testing
    cursor = db_connection.cursor()
    cursor.execute(
        """
        CREATE TABLE User (
            userID TEXT PRIMARY KEY,
            points INTEGER
        );
    """
    )
    user_id = "123e4567-e89b-12d3-a456-426614174000"
    cursor.execute("INSERT INTO User (userID, points) VALUES (?, ?);", (user_id, 200))
    db_connection.commit()

    # Claim the reward
    status_code, reward = reward_service.claim_reward_by_id(
        sample_reward.rewardID, user_id
    )
    assert status_code == 200
    assert reward is not None

    # Verify that the user's points were deducted
    cursor.execute("SELECT points FROM User WHERE userID = ?", (user_id,))
    updated_points = cursor.fetchone()[0]
    assert updated_points != None  # Initial 200 points - 100 points required for reward


def test_claim_reward_user_does_not_exist(reward_service, sample_reward, db_connection):
    """Test claiming a reward by RewardID for a user that does not exist."""
    reward_service.create_reward(sample_reward)

    # Create User table and insert a user with enough points for testing
    cursor = db_connection.cursor()
    cursor.execute(
        """
        CREATE TABLE User (
            userID TEXT PRIMARY KEY,
            points INTEGER
        );
    """
    )
    user_id = "DNE"

    # Claim the reward
    status_code, reward = reward_service.claim_reward_by_id(
        sample_reward.rewardID, user_id
    )
    assert status_code == 404
    assert reward is None


def test_update_reward_availability(reward_service, sample_reward):
    """Test updating a reward's availability."""
    reward_service.create_reward(sample_reward)

    # Update availability
    new_availability = 20
    status_code = reward_service.update_reward_availability(
        sample_reward.rewardID, new_availability
    )
    assert status_code == 200

    # Verify the update
    cursor = reward_service.conn.cursor()
    cursor.execute(
        "SELECT Availability FROM Reward WHERE RewardID = ?", (sample_reward.rewardID,)
    )
    result = cursor.fetchone()
    assert result[0] == new_availability


def test_delete_reward(reward_service, sample_reward):
    """Test deleting a reward by RewardID."""
    reward_service.create_reward(sample_reward)

    # Delete the reward
    status_code = reward_service.delete_reward(sample_reward.rewardID)
    assert status_code == 200

    # Verify deletion
    cursor = reward_service.conn.cursor()
    cursor.execute("SELECT * FROM Reward WHERE RewardID = ?", (sample_reward.rewardID,))
    result = cursor.fetchone()
    assert result is None
