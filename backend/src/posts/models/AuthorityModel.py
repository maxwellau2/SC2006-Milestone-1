from pydantic import BaseModel
from typing import Optional


class Authority(BaseModel):
    user_id: str
    authority_name: str
