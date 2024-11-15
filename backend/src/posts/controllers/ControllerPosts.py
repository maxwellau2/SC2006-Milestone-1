import os
from fastapi import APIRouter, FastAPI, File, HTTPException, UploadFile
from typing import Optional, List

from fastapi.responses import FileResponse
from src.posts.models.PostModel import Post
from src.posts.services.PostService import PostService
from pydantic import BaseModel

router = APIRouter(prefix="/posts")


@router.post("/posts/", status_code=200)
async def create_post(
    user_id: str,
    title: Optional[str],
    description: Optional[str],
    image: Optional[UploadFile] = File(None),
    post_id: Optional[str] = None,
):
    """Create a new post with authority and user information based on user_id."""

    # Define the image path based on the identifier and original extension
    file_extension = image.filename.split(".")[-1].lower()
    image_dir = "img/postImages"
    image_path = os.path.join(image_dir, f"{user_id}.{file_extension}")
    # Ensure the directory exists
    os.makedirs(image_dir, exist_ok=True)

    # Create an empty post with provided details
    post = Post.make_empty_post_with_details(
        title=title,
        description=description,
    )
    if post_id:
        post.post_id = post_id

    # Define the image path based on the identifier and original extension
    file_extension = image.filename.split(".")[-1].lower()
    image_path = os.path.join(image_dir, f"{post.post_id}.{file_extension}")

    # Save the image
    try:
        with open(image_path, "wb") as image_file:
            image_file.write(await image.read())
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to save image: {str(e)}",
        )

    post.image_path = image_path

    # Use PostService to create a post with authority info
    status_code, created_post = PostService.create_post_with_authority(user_id, post)
    if status_code == 201:
        return {
            "post_id": created_post.post_id,
            "title": created_post.title,
            "description": created_post.description,
            "image_path": created_post.image_path,
        }
    elif status_code == 404:
        raise HTTPException(status_code=404, detail="User or authority not found")
    else:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/posts/{post_id}", response_model=Post)
def get_post(post_id: str):
    """Retrieve a post by post_id."""
    status_code, post = PostService.read_entry(post_id)
    if status_code == 200:
        return post
    elif status_code == 404:
        raise HTTPException(status_code=404, detail="Post not found")
    else:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/posts/image/{post_id}", response_class=FileResponse)
async def get_post_image(post_id: str):
    """Retrieve the image corresponding to the post identifier."""
    # Define the path to the images directory
    image_dir = "img/postImages"
    print("hello!")
    # Construct the image file path (assuming .png extension)
    # check if post_id is a png file
    print(post_id)
    if os.path.isfile(os.path.join(image_dir, f"{post_id}.png")):
        image_path = os.path.join(image_dir, f"{post_id}.png")
    # check if post_id is a jpg
    elif os.path.isfile(os.path.join(image_dir, f"{post_id}.jpg")):
        image_path = os.path.join(image_dir, f"{post_id}.jpg")
    elif os.path.isfile(os.path.join(image_dir, f"{post_id}.jpeg")):
        image_path = os.path.join(image_dir, f"{post_id}.jpeg")
    else:
        image_path = os.path.join(image_dir, f"default.png")
    # read the file contents
    print(image_path)
    return FileResponse(image_path, media_type="image/png")


@router.get("/posts/", response_model=List[Post])
def get_all_posts():
    """Retrieve all posts."""
    status_code, posts = PostService.read_all_entries()
    if status_code == 200:
        return posts
    else:
        raise HTTPException(status_code=500, detail="Internal server error")


class PostUpdateRequest(BaseModel):
    title: Optional[str]
    description: Optional[str]
    image_path: Optional[str]
    authority_name: Optional[str]
    user_id: Optional[str]


@router.put("/posts/{post_id}", response_model=Post)
def update_post(post_id: str, request: PostUpdateRequest):
    """Update an existing post."""
    status_code = PostService.update_entry(
        post_id=post_id,
        new_title=request.title,
        new_description=request.description,
        new_image_path=request.image_path,
        new_authority_name=request.authority_name,
        new_user_id=request.user_id,
    )
    if status_code == 200:
        _, updated_post = PostService.read_entry(post_id)
        return updated_post
    elif status_code == 404:
        raise HTTPException(status_code=404, detail="Post not found")
    else:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.delete("/posts/{post_id}", status_code=204)
def delete_post(post_id: str):
    """Delete a post by post_id."""
    status_code = PostService.delete_entry(post_id)
    if status_code == 200:
        return
    elif status_code == 404:
        raise HTTPException(status_code=404, detail="Post not found")
    else:
        raise HTTPException(status_code=500, detail="Internal server error")
