from typing import Optional
from pydantic import BaseModel, Field


class MyRewards(BaseModel):
    reward_id: str = Field(...)
    user_id: str = Field(...)
    expiry: int
    giftcode: Optional[str]
