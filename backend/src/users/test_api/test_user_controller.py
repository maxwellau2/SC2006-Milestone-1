import pytest
import requests
from fastapi import status
from uuid import UUID

BASE_URL = "http://localhost:8000/users/users"
TEST_USER_ID = UUID("123e4567-e89b-12d3-a456-426614174000")


@pytest.fixture(scope="module")
def client():
    """Setup base URL for the API."""
    return BASE_URL


def test_read_all_users(client):
    """Test retrieving all users."""
    response = requests.get(f"{client}/all")
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)


def test_read_user(client):
    """Test retrieving a user by ID."""
    response = requests.get(f"{client}/", params={"user_id": TEST_USER_ID})
    assert response.status_code == status.HTTP_200_OK
    user = response.json()
    assert user["userID"] == str(TEST_USER_ID)
    assert user["userName"] == "jingxiang1"


def test_create_user(client):
    """Test creating a new user."""
    new_user_data = {
        "userName": "new_user",
        "passwordHash": "hashed_password",
        "emailAddress": "new_user@example.com",
        "loginStatus": False,
        "points": 0,
        "notificationPreference": "email",
        "notificationEnabled": True,
        "isAuthority": False,
        "isModerator": False,
    }
    response = requests.post(f"{client}/", json=new_user_data)
    assert response.status_code == status.HTTP_200_OK
    user = response.json()
    assert user["userName"] == new_user_data["userName"]
    assert user["emailAddress"] == new_user_data["emailAddress"]


def test_update_user_points(client):
    """Test updating a user's points."""
    update_data = {"user_id": str(TEST_USER_ID), "points": 50}
    response = requests.put(f"{client}/updatepoints", params=update_data)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["detail"] == "User points updated successfully."


def test_update_user(client):
    """Test updating a user's details."""
    update_data = {
        "userName": "updated_user",
        "emailAddress": "updated_user@example.com",
    }
    response = requests.put(f"{client}/{TEST_USER_ID}/update", json=update_data)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["detail"] == "User updated successfully."


def test_get_profile_picture(client):
    """Test retrieving a user's profile picture."""
    response = requests.get(f"{client}/profilePicture/{TEST_USER_ID}")
    assert response.status_code == status.HTTP_200_OK
    assert response.headers["content-type"] == "image/png"


def test_update_profile_picture(client):
    """Test updating a user's profile picture."""
    with open("src/users/test_api/test_profile_picture.png", "rb") as file:
        response = requests.post(
            f"{client}/profilePicture/{TEST_USER_ID}", files={"file": file}
        )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["detail"] == "Profile picture updated successfully."
