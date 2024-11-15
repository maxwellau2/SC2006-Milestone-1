from fastapi import APIRouter, Form, HTTPException, status, Response
from fastapi.responses import JSONResponse
from src.users.services.AuthService import AuthService
from src.users.models.UserModels import (
    UserRegister,
    UserCreate,
    UserRead,
    User,
    UserLogin,
    StatusResponse,
)
import sqlite3

from src.users.models.PasswordReset import PasswordResetRequest, PasswordReset

router = APIRouter(prefix="/public")

conn = sqlite3.connect("database/users.db")
auth_service = AuthService(conn)  # Instantiate the AuthService


@router.post("/register", response_model=StatusResponse)
async def register_user(user: UserRegister):
    """Register a new user."""
    status_code, user_read = auth_service.register(
        user.userName, user.password, user.emailAddress
    )
    print("Poop")
    if status_code == 400:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to register user: User already exists.",
        )
    elif status_code == 200:
        return Response(
            content="User registered successfully.", status_code=status.HTTP_200_OK
        )
    elif status_code == 422:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Failed to register user: Username or email already exists.",
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to register user.",
        )


@router.post("/login", response_model=str)
async def login_user(user: UserLogin):
    """Login a user."""
    status_code, res = auth_service.login(user.username, user.password)
    if status_code == 200:
        # Set the cookie in the response
        response = JSONResponse(
            content={
                "token": res["token"],
                "user_id": res["user_id"],
                "isAuthority": res["isAuthority"],
                "isModerator": res["isModerator"],
            },
            status_code=status_code,
        )
        response.set_cookie(
            key="access_token",
            value=res["token"],
            httponly=True,  # This makes the cookie inaccessible to JavaScript (increases security)
            max_age=86400,  # Set the cookie to expire after 1 day (86400 seconds)
            samesite="Lax",  # Adjust according to your requirements (Lax, Strict, None)
        )
        response.set_cookie(
            key="user_id",
            value=res["user_id"],
            httponly=False,  # make accessible to JavaScript
            max_age=86400,  # Set the cookie to expire after 1 day (86400 seconds)
            samesite="Lax",  # Adjust according to your requirements (Lax, Strict, None)
        )
        return response
    elif status_code == 401:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Failed to login user: Invalid credentials.",
        )
    elif status_code == 404:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Failed to login user: User not found.",
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to login user.",
        )


@router.get("/verify/{verification_key}")
async def verify_user(verification_key: str):
    """Verify a user with the provided verification key."""
    status_code, response = auth_service.verify_user(verification_key)
    print(status_code, response)
    if status_code == 200:
        return JSONResponse(response)
    elif status_code == 404:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid or expired verification key.",
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to verify user.",
        )


@router.post("/password-reset-request/")
async def request_password_reset(data: PasswordResetRequest):
    """Request a password reset email."""
    status_code, response = auth_service.send_password_reset_email(data.email)
    if status_code == 200:
        return JSONResponse(
            content={"message": "Password reset email sent successfully."},
            status_code=status_code,
        )
    elif status_code == 404:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Failed to send password reset email: Email not found.",
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to send password reset email.",
        )


@router.post("/password-reset/")
async def reset_password(data: PasswordReset):
    """Reset a user's password using a verification key."""
    status_code, response = auth_service.reset_password(
        data.verification_key, data.new_password
    )
    if status_code == 200:
        return JSONResponse(
            content={"message": "Password reset successfully."}, status_code=status_code
        )
    elif status_code == 404:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid or expired verification key.",
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to reset password.",
        )
