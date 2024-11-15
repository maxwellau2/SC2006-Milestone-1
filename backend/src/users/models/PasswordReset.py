from pydantic import BaseModel, Field
import uuid


class ResetPassword(BaseModel):
    userID: uuid.UUID
    verificationKey: str

    @classmethod
    def create_reset_request(cls, user_id: uuid.UUID) -> "ResetPassword":
        """Factory method to create a new ResetPassword instance with a unique verification key."""
        return cls(
            userID=user_id,
            verificationKey=str(uuid.uuid4()),  # Generate a unique verification key
        )


class PasswordResetRequest(BaseModel):
    email: str


class PasswordReset(BaseModel):
    verification_key: str
    new_password: str
