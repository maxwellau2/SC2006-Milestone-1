import pytest
import requests
from fastapi import status
from uuid import uuid4
import os


BASE_URL = "http://localhost:8000/posts/posts/posts"
TEST_USER_ID = "123e4567-e89b-12d3-a456-426614174010"  # Example user ID
TEST_POST_ID = "123e4567-e89b-12d3-a456-426614174927"
IMAGE_DIR = "img/postImages"
IMAGE_PATH = "src/posts/test_api/hotdogdog.png"


@pytest.fixture(scope="module")
def client():
    """Setup base URL for the API."""
    return BASE_URL


def test_create_post(client):
    """Test creating a new post with an image upload."""
    post_data = {
        "user_id": TEST_USER_ID,
        "title": "Test Post",
        "description": "Test description for post",
        "post_id": TEST_POST_ID,
    }

    # Ensure a test image exists
    with open(IMAGE_PATH, "wb") as file:
        file.write(os.urandom(1024))  # Write random binary content as a test image

    # Prepare form data for fields and file
    with open(IMAGE_PATH, "rb") as file:
        files = {"image": (IMAGE_PATH, file, "image/png")}
        response = requests.post(
            f"{client}/", params=post_data, json=post_data, files=files
        )

    # Check response
    assert (
        response.status_code == status.HTTP_200_OK
    ), f"Failed to create post: {response.json()}"
    post = response.json()
    assert post["title"] == post_data["title"]
    assert post["description"] == post_data["description"]


def test_get_post(client):
    """Test retrieving a post by ID."""
    response = requests.get(f"{client}/{TEST_POST_ID}")
    assert response.status_code == status.HTTP_200_OK, "Failed to retrieve post"
    post = response.json()
    assert post["post_id"] == TEST_POST_ID


def test_get_post_image(client):
    """Test retrieving the image of a post by ID."""
    response = requests.get(f"{client}/image/{TEST_POST_ID}")
    assert response.status_code == status.HTTP_200_OK, "Failed to retrieve post image"
    assert response.headers["content-type"] in ["image/png", "image/jpeg"]


def test_get_all_posts(client):
    """Test retrieving all posts."""
    response = requests.get(f"{client}/")
    assert response.status_code == status.HTTP_200_OK, "Failed to retrieve all posts"
    posts = response.json()
    assert isinstance(posts, list), "Expected a list of posts"


def test_update_post(client):
    """Test updating an existing post."""
    update_data = {
        "title": "Updated Test Post",
        "description": "Updated description",
        "image_path": "Updated image path",
        "authority_name": "Updated Authority",
        "user_id": TEST_USER_ID,
    }
    response = requests.put(f"{client}/{TEST_POST_ID}", json=update_data)
    assert response.status_code == status.HTTP_200_OK, "Failed to update post"
    updated_post = response.json()
    assert updated_post["title"] == update_data["title"]
    assert updated_post["description"] == update_data["description"]


def test_delete_post(client):
    """Test deleting a post by ID."""
    response = requests.delete(f"{client}/{TEST_POST_ID}")
    assert response.status_code == status.HTTP_204_NO_CONTENT, "Failed to delete post"


def test_get_deleted_post(client):
    """Test that the deleted post is no longer available."""
    response = requests.get(f"{client}/{TEST_POST_ID}")
    assert (
        response.status_code == status.HTTP_404_NOT_FOUND
    ), "Deleted post still retrievable"


def cleanup_test_files():
    """Clean up any test image files."""
    if os.path.exists(IMAGE_PATH):
        os.remove(IMAGE_PATH)
    if os.path.exists(f"{IMAGE_DIR}/{TEST_POST_ID}.png"):
        os.remove(f"{IMAGE_DIR}/{TEST_POST_ID}.png")


# Run cleanup after all tests
@pytest.fixture(scope="module", autouse=True)
def cleanup():
    yield
    cleanup_test_files()
