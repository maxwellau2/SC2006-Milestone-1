import pytest
import requests
from fastapi import status
from uuid import uuid4

BASE_URL = "http://localhost:8000/rewards/rewards"
TEST_REWARD_ID = "123e4567-e89b-12d3-a456-426614174000"


@pytest.fixture(scope="module")
def client():
    """Setup base URL for the API."""
    return BASE_URL


def test_read_all_rewards(client):
    """Test retrieving all rewards."""
    response = requests.get(f"{client}/all")
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)


def test_read_reward_by_id(client):
    """Test retrieving a reward by ID."""
    response = requests.get(f"{client}/{TEST_REWARD_ID}")
    if response.status_code == status.HTTP_200_OK:
        reward = response.json()
        assert reward["rewardID"] == TEST_REWARD_ID
    elif response.status_code == status.HTTP_404_NOT_FOUND:
        assert response.json()["detail"] == "Reward not found"


def test_create_reward(client):
    """Test creating a new reward with multipart form data for file and query parameters for other fields."""

    # Prepare query parameters for creating a reward
    reward_data = {
        "description": "Test Reward",
        "pointsRequired": 100,
        "availability": 10,
        "validity": 30,  # Optional field for validity in days
    }

    # Open the image file to be uploaded (make sure this file exists)
    with open("src/rewards/test_api/reward_image.png", "rb") as file:
        # Prepare the file part of the request
        files = {"file": ("reward_image.png", file, "image/png")}

        # Send POST request with query parameters and file
        response = requests.post(
            f"{client}/",
            params=reward_data,  # Send non-file parameters as query parameters
            files=files,
        )

    # Validate the response
    assert response.status_code == status.HTTP_200_OK, "Failed to create reward"
    reward = response.json()

    # Validate response content
    assert reward["description"] == reward_data["description"], "Description mismatch"
    assert reward["pointsRequired"] == reward_data["pointsRequired"], "Points mismatch"
    assert (
        reward["availability"] == reward_data["availability"]
    ), "Availability mismatch"
    assert "rewardID" in reward, "Missing reward ID in response"


def test_update_reward_quantity(client):
    """Test updating reward quantity."""
    response = requests.put(
        f"{client}/{TEST_REWARD_ID}/quantity", json={"quantity": 20}
    )
    if response.status_code == status.HTTP_200_OK:
        assert response.json()["detail"] == "Reward quantity updated successfully."
    elif response.status_code == status.HTTP_404_NOT_FOUND:
        assert response.json()["detail"] == "Reward not found"


def test_check_reward_validity(client):
    """Test checking reward validity."""
    response = requests.get(f"{client}/{TEST_REWARD_ID}/validity")
    if response.status_code == status.HTTP_200_OK:
        assert "is_valid" in response.json()
    elif response.status_code == status.HTTP_404_NOT_FOUND:
        assert response.json()["detail"] == "Reward not found"


def test_generate_encoded_reward(client):
    """Test generating a Base64-encoded reward string."""
    response = requests.post(
        f"{client}/{TEST_REWARD_ID}/generate", json={"duration": 30}
    )
    if response.status_code == status.HTTP_200_OK:
        assert "encoded_reward" in response.json()
    elif response.status_code == status.HTTP_404_NOT_FOUND:
        assert response.json()["detail"] == "Reward not found"


def test_delete_reward(client):
    """Test deleting a reward by ID."""
    response = requests.delete(f"{client}/{TEST_REWARD_ID}")
    if response.status_code == status.HTTP_200_OK:
        assert response.json()["detail"] == "Reward deleted successfully."
    elif response.status_code == status.HTTP_404_NOT_FOUND:
        assert response.json()["detail"] == "Reward not found"


def test_get_reward_image(client):
    """Test retrieving a reward's image."""
    response = requests.get(f"{client}/{TEST_REWARD_ID}/image")
    if response.status_code == status.HTTP_200_OK:
        assert response.headers["content-type"] == "image/png"
    elif response.status_code == status.HTTP_404_NOT_FOUND:
        assert response.json()["detail"] == "Image not found"


def test_upload_reward_image(client):
    """Test uploading a reward image."""
    with open("src/rewards/test_api/reward_image.png", "rb") as file:
        files = {"file": file}
        response = requests.post(f"{client}/{TEST_REWARD_ID}/image", files=files)
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["detail"] == "Image uploaded successfully."


def test_get_my_rewards(client):
    """Test retrieving rewards claimed by a specific user."""
    user_id = "sample_user"
    response = requests.get(f"{client}/myrewards/{user_id}")
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)


def test_claim_reward(client):
    """Test claiming a reward by ID."""
    user_id = "sample_user"
    response = requests.post(
        f"{client}/claim/{TEST_REWARD_ID}", json={"user_id": user_id}
    )
    if response.status_code == status.HTTP_200_OK:
        assert response.json()["detail"] == "Reward claimed successfully."
    elif response.status_code == status.HTTP_404_NOT_FOUND:
        assert response.json()["detail"] == "Reward not found"
    elif response.status_code == status.HTTP_403_FORBIDDEN:
        assert response.json()["detail"] == "Insuffient points"


def test_update_reward(client):
    """Test updating a reward's details."""
    update_data = {
        "description": "Updated Reward",
        "pointsRequired": 150,
        "availability": 5,
        "validity": 60,
    }
    response = requests.put(f"{client}/update/{TEST_REWARD_ID}", json=update_data)
    if response.status_code == status.HTTP_200_OK:
        assert response.json()["detail"] == "Reward updated successfully."
    elif response.status_code == status.HTTP_404_NOT_FOUND:
        assert response.json()["detail"] == "Reward not found"
    elif response.status_code == status.HTTP_403_FORBIDDEN:
        assert response.json()["detail"] == "Insuffient points"
