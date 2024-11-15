from pydantic import BaseModel
from typing import Optional


class Report(BaseModel):
    user_id: str
    relevance: int
    severity: int
    urgency: int
    status: str = "Pending"
    report_id: str
    description: Optional[str]
    image_path: Optional[str]
    title: Optional[str]
    datetime: int
    location: str
    points: int = 0
    ollama_description: str = ""
    authority_id: str = ""
