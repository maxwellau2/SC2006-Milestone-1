from pydantic import BaseModel
from typing import Literal
import uuid

from src.users.models.UserModels import UserCreate


class UnverifiedUser(BaseModel):
    userID: uuid.UUID
    userName: str
    passwordHash: str
    emailAddress: str
    loginStatus: bool
    points: int
    notificationPreference: Literal["email", "sms", "push"]
    notificationEnabled: bool
    isAuthority: bool
    isModerator: bool
    verificationKey: str

    @classmethod
    def create_unverified(
        cls, userName: str, passwordHash: str, emailAddress: str
    ) -> "UnverifiedUser":
        """Factory method to create a new UnverifiedUser with a unique verification key."""
        return cls(
            userID=uuid.uuid4(),
            userName=userName,
            passwordHash=passwordHash,
            emailAddress=emailAddress,
            loginStatus=False,
            points=0,
            notificationPreference="email",
            notificationEnabled=True,
            isAuthority=False,
            isModerator=False,
            verificationKey=str(uuid.uuid4()),  # unique verification key
        )

    def to_verified_user(self) -> "UserCreate":
        """Convert UnverifiedUser to UserCreate, removing the verification key."""
        return UserCreate(
            userID=self.userID,
            userName=self.userName,
            passwordHash=self.passwordHash,
            emailAddress=self.emailAddress,
            loginStatus=self.loginStatus,
            points=self.points,
            notificationPreference=self.notificationPreference,
            notificationEnabled=self.notificationEnabled,
            isAuthority=self.isAuthority,
            isModerator=self.isModerator,
        )
