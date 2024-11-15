from pydantic import BaseModel
from typing import Optional
import uuid
import time


class Post(BaseModel):
    post_id: str
    title: Optional[str]
    description: Optional[str]
    image_path: Optional[str]
    authority_name: str
    user_name: Optional[str]
    user_id: Optional[str]
    time: int = int(time.time())

    @staticmethod
    def make_empty_post() -> "Post":
        """Factory method to create an empty Post object with default values."""
        return Post(
            post_id="",  # Empty post ID
            title=None,  # No title
            description=None,  # No description
            image_path=None,  # No image path
            authority_name="",  # Authority name must be provided
            user_name="",
            user_id="",
        )

    @staticmethod
    def make_empty_post_with_details(
        title: str, description: str, image_path: str = ""
    ) -> "Post":
        """Factory method to create an empty Post object with default values."""
        return Post(
            post_id=str(uuid.uuid4()),  # Empty post ID
            title=title,  # No title
            description=description,  # No description
            image_path=image_path,  # No image path
            authority_name="",  # Authority name must be provided
            user_name="",
            user_id="",
            time=int(time.time()),
        )
