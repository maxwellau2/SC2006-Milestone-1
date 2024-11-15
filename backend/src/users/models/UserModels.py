from pydantic import BaseModel, Field
import uuid
from typing import Literal


# ========= pydantic models for FASTAPI requests ============
# ========= generically, they are called DTOS (Data Transfer Objects) ==========
class UserCreate(BaseModel):
    userID: uuid.UUID = Field(default_factory=uuid.uuid4)
    userName: str
    passwordHash: str
    emailAddress: str
    loginStatus: bool
    points: int
    notificationPreference: Literal["email", "sms", "push"]
    notificationEnabled: bool
    isAuthority: bool
    isModerator: bool


class UserRegister(BaseModel):
    userName: str
    password: str
    emailAddress: str


class UserUpdate(BaseModel):
    userName: str
    emailAddress: str


class UserLogin(BaseModel):
    username: str
    password: str


class UserRead(BaseModel):
    userID: uuid.UUID
    userName: str
    emailAddress: str
    loginStatus: bool
    points: int
    notificationEnabled: bool
    isAuthority: bool
    isModerator: bool


class StatusResponse(BaseModel):
    status: int
    detail: str


# ============== Entity class for the User model ===============
class User:
    def __init__(
        self,
        userName: str,
        passwordHash: str,
        emailAddress: str,
        loginStatus: bool,
        points: int,
        notificationPreference: Literal["email", "sms", "push"],
        notificationEnabled: bool,
        isAuthority: bool,
        isModerator: bool,
        userID: uuid.UUID = None,
    ):
        self.userID: uuid.UUID = userID if userID else uuid.uuid4()
        self.userName: str = userName
        self.passwordHash: str = passwordHash
        self.emailAddress: str = emailAddress
        self.loginStatus: bool = loginStatus
        self.points: int = points
        self.notificationPreference: Literal["email", "sms", "push"] = (
            notificationPreference
        )
        self.notificationEnabled: bool = notificationEnabled
        self.isAuthority: bool = isAuthority
        self.isModerator: bool = isModerator

    def __repr__(self) -> str:
        return (
            f"User(userID={self.userID}, userName={self.userName}, email={self.emailAddress}, "
            f"loginStatus={self.loginStatus}, points={self.points}, "
            f"notificationEnabled={self.notificationEnabled}, isAuthority={self.isAuthority}, "
            f"isModerator={self.isModerator})"
        )
