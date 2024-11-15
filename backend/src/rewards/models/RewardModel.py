# Reward.py
import uuid
import base64
from datetime import datetime, timedelta
from pydantic import BaseModel, Field


class RewardUpdate(BaseModel):
    description: str
    pointsRequired: int = Field(..., gt=0)  # Points required must be positive
    validity: int = Field(..., ge=0)  # Validity timestamp must be non-negative
    availability: int = Field(..., ge=0)  # Availability must be non-negative


class Reward(BaseModel):
    rewardID: str = Field(default_factory=lambda: str(uuid.uuid4()))
    description: str
    pointsRequired: int = Field(..., gt=0)  # Points required must be positive
    validity: int = Field(..., ge=0)  # Validity timestamp must be non-negative
    availability: int = Field(..., ge=0)  # Availability must be non-negative

    def generateReward(self, duration: int) -> str:
        """
        Generates a Base64-encoded reward string with expiration timestamp.
        """
        expiration_time = datetime.now() + timedelta(days=duration)
        expire_timestamp = int(expiration_time.timestamp())
        self.validity = expire_timestamp

        recipe = f"{self.description}+{expire_timestamp}"
        encoded_recipe = base64.b64encode(recipe.encode()).decode()
        return encoded_recipe

    def decodeReward(self, encoded_recipe: str) -> str:
        """
        Decodes a Base64-encoded reward back to its original form.
        """
        decoded_recipe = base64.b64decode(encoded_recipe).decode()
        return decoded_recipe

    def is_valid(self) -> bool:
        """
        Checks if the reward is still valid based on its validity timestamp.
        """
        current_timestamp = int(datetime.now().timestamp())
        return current_timestamp < self.validity
