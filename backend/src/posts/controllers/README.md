---

# Post API Documentation

This API enables managing posts in an application, including creating, updating, retrieving, and deleting posts, as well as handling associated images. The API is built using FastAPI, with endpoints organized under the `/posts` prefix.

## Table of Contents
- [Overview](#overview)
- [Endpoints](#endpoints)
  - [Create a Post](#create-a-post)
  - [Get a Post](#get-a-post)
  - [Get Post Image](#get-post-image)
  - [Get All Posts](#get-all-posts)
  - [Update a Post](#update-a-post)
  - [Delete a Post](#delete-a-post)

## Overview

The `Post API` provides endpoints for:
- Creating new posts, with an optional image upload.
- Retrieving individual or all posts.
- Fetching post images based on post identifiers.
- Updating or deleting posts by their unique identifiers.

The API uses the `PostService` class to manage database operations for the `Post` model.

---

## Endpoints

### Create a Post

-   **URL**: `/posts/`
-   **Method**: `POST`
-   **Description**: Creates a new post with optional user information, image, title, and description. Stores images under `img/postImages`.

#### Request Parameters

-   `user_id` (str): User identifier for the post.
-   `title` (Optional[str]): Title of the post.
-   `description` (Optional[str]): Description of the post.
-   `image` (Optional[UploadFile]): Image file to associate with the post.
-   `post_id` (Optional[str]): Custom post ID (optional, auto-generated if not provided).

#### Response

-   **Status Code**: `200` if successful, `404` if user/authority not found, or `500` if an internal server error occurs.
-   **Response Body**:
    ```json
    {
        "post_id": "string",
        "title": "string",
        "description": "string",
        "image_path": "string"
    }
    ```

### Get a Post

-   **URL**: `/posts/{post_id}`
-   **Method**: `GET`
-   **Description**: Retrieves a post by its `post_id`.

#### Request Parameters

-   `post_id` (str): Identifier of the post to retrieve.

#### Response

-   **Status Code**: `200` if found, `404` if not found, or `500` if an internal server error occurs.
-   **Response Model**: `Post`

### Get Post Image

-   **URL**: `/posts/image/{post_id}`
-   **Method**: `GET`
-   **Description**: Retrieves the image associated with a post. If the specified image is not found, a default image is returned.

#### Request Parameters

-   `post_id` (str): Identifier of the post image to retrieve.

#### Response

-   **Response Class**: `FileResponse` - returns the image file directly.

### Get All Posts

-   **URL**: `/posts/`
-   **Method**: `GET`
-   **Description**: Retrieves all posts in the database, ordered by creation time.

#### Response

-   **Status Code**: `200` if successful, `500` if an internal server error occurs.
-   **Response Model**: `List[Post]`

### Update a Post

-   **URL**: `/posts/{post_id}`
-   **Method**: `PUT`
-   **Description**: Updates fields of an existing post.

#### Request Parameters

-   `post_id` (str): Identifier of the post to update.
-   **Request Body**:
    ```json
    {
        "title": "Optional[str]",
        "description": "Optional[str]",
        "image_path": "Optional[str]",
        "authority_name": "Optional[str]",
        "user_id": "Optional[str]"
    }
    ```

#### Response

-   **Status Code**: `200` if updated, `404` if post not found, or `500` if an internal server error occurs.
-   **Response Model**: `Post`

### Delete a Post

-   **URL**: `/posts/{post_id}`
-   **Method**: `DELETE`
-   **Description**: Deletes a post by its `post_id`.

#### Request Parameters

-   `post_id` (str): Identifier of the post to delete.

#### Response

-   **Status Code**: `204` if successful, `404` if post not found, or `500` if an internal server error occurs.

---

This documentation should provide a comprehensive guide for developers working with the Post API endpoints. Let me know if you need further customization or specific details on any endpoint!
