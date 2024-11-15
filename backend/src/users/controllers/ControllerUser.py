import os
from fastapi import APIRouter, File, HTTPException, status, Response
from fastapi.responses import FileResponse, JSONResponse
from typing import Optional
import sqlite3
import uuid

from src.users.models.UserModels import (
    UserRegister,
    UserCreate,
    UserRead,
    User,
    UserLogin,
    StatusResponse,
    UserUpdate,
)
from src.users.services.UserService import UserService

router = APIRouter(prefix="/users")

conn = sqlite3.connect("database/users.db")
user_service = UserService(conn)  # Instantiate the UserService


@router.get("/all", response_model=list[UserRead])
async def read_all_users():
    """Read all users."""
    status_code, users = user_service.read_all_users()
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail="Failed to retrieve users.")
    return users


@router.get("/", response_model=Optional[UserRead])
async def read_user(user_id: uuid.UUID):
    """Read a user's details by user ID."""
    status_code, user = user_service.read_user(user_id)
    if status_code == 404:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    elif status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve user.",
        )
    return user


@router.post("/", response_model=UserRead)
async def create_user(user: UserCreate):
    """Create a new user."""
    status_code, user_read = user_service.create_user(User(**user.dict()))
    if status_code == 201:
        return user_read
    elif status_code == 400:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to create user: User ID already exists.",
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create user.",
        )


@router.put("/updatepoints")
async def update_user_points(user_id: uuid.UUID, points: int):
    """Update user points."""
    status_code = user_service.update_user_points(user_id, points)
    if status_code == 404:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    elif status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update user points.",
        )
    return {"detail": "User points updated successfully."}


@router.put("/{user_id}/update", response_model=dict)
async def update_user(user_id: uuid.UUID, user: UserUpdate):
    """Update a user."""
    status_code = user_service.update_user(user_id, user=user)
    if status_code == 404:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    elif status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update user.",
        )
    return {"detail": "User updated successfully."}


@router.delete("/")
async def delete_user(user_id: uuid.UUID):
    """Delete a user."""
    status_code = user_service.delete_user(user_id)
    if status_code == 404:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    elif status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete user.",
        )
    return {"detail": "User deleted successfully."}


@router.delete("/wipe", response_model=dict)
async def wipe_users():
    """Wipe all users from the database."""
    status_code = user_service.wipeClean()
    if status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to wipe users.",
        )
    return {"detail": "All users wiped successfully."}


@router.get("/profilePicture/{user_id}", response_class=Response)
async def get_profile_picture(user_id: uuid.UUID):
    """Retrieve the profile picture of a user."""
    # Define the path to the images directory
    image_dir = "img/profilepics"
    # Construct the image file path (assuming .png extension)
    image_path = f"{image_dir}/{user_id}.png"

    # Check if the image exists
    if not os.path.isfile(image_path):
        return FileResponse(f"{image_dir}/default.png", media_type="image/png")

    # Return the image file
    return FileResponse(image_path, media_type="image/png")


@router.post("/profilePicture/{user_id}")
async def update_profile_picture(user_id: uuid.UUID, file: bytes = File(...)):
    """Update the profile picture of a user."""
    # check if user exists
    if not user_service.check_user_exists(str(user_id)):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    # Define the path to the images directory
    image_dir = "img/profilepics"
    # Construct the image file path (assuming .png extension)
    image_path = f"{image_dir}/{user_id}.png"
    # update the image
    with open(image_path, "wb") as f:
        f.write(file)
    # return success
    return {"detail": "Profile picture updated successfully."}
