import pytest
import sqlite3
import time
import uuid
import os
from src.posts.services.PostService import PostService
from src.posts.models.PostModel import Post


# Use a temporary database file for testing
@pytest.fixture
def sample_post():
    """Provides a sample Post object for testing."""
    return Post(
        post_id=str(uuid.uuid4()),
        title="Test Title",
        description="Test Description",
        image_path="test/path.jpg",
        authority_name="Authority",
        user_name="User",
        user_id="123e4567-e89b-12d3-a456-426614174001",
        time=int(time.time()),
    )


def test_create_entry_success(sample_post):
    """Test successfully creating a post entry."""
    status_code, created_post = PostService.create_entry(sample_post)
    assert status_code == 201
    assert created_post is not None
    assert created_post.post_id == sample_post.post_id


def test_create_entry_duplicate(sample_post):
    """Test inserting a duplicate post_id, expecting failure."""
    PostService.create_entry(sample_post)
    status_code, created_post = PostService.create_entry(sample_post)
    assert status_code != 201
    assert created_post is None


def test_read_all_entries(sample_post):
    """Test reading all existing post entries."""
    PostService.create_entry(sample_post)
    status_code, posts = PostService.read_all_entries()
    print(posts)
    assert status_code == 200
    assert posts is not None


def test_read_entry_success(sample_post):
    """Test reading an existing post entry."""
    PostService.create_entry(sample_post)
    status_code, post = PostService.read_entry(sample_post.post_id)
    assert status_code == 200
    assert post is not None
    assert post.post_id == sample_post.post_id


def test_read_entry_not_found():
    """Test reading a non-existing post entry."""
    status_code, post = PostService.read_entry("non_existing_id")
    assert status_code == 404
    assert post is None


def test_update_entry_success(sample_post):
    """Test updating an existing post entry."""
    PostService.create_entry(sample_post)
    new_title = "Updated Title"
    new_description = "Updated Description"
    status_code = PostService.update_entry(
        post_id=sample_post.post_id,
        new_title=new_title,
        new_description=new_description,
    )
    assert status_code == 200
    _, updated_post = PostService.read_entry(sample_post.post_id)
    assert updated_post.title == new_title
    assert updated_post.description == new_description


def test_delete_entry_success(sample_post):
    """Test deleting an existing post entry."""
    PostService.create_entry(sample_post)
    status_code = PostService.delete_entry(sample_post.post_id)
    assert status_code == 200
    status_code, post = PostService.read_entry(sample_post.post_id)
    assert status_code == 404
    assert post is None
