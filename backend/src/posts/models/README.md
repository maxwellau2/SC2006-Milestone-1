# Models Documentation

This document describes the `Authority` and `Post` models used within the application, defined using Pydantic for data validation and serialization.

## Table of Contents

-   [Authority Model](#authority-model)
    -   [Fields](#authority-fields)
-   [Post Model](#post-model)
    -   [Fields](#post-fields)
    -   [Methods](#post-methods)

---

## Authority Model

The `Authority` model represents an authority entity within the application. It includes fields for `user_id` and `authority_name` and is used primarily by the `AuthorityService`.

### Authority Fields

-   **`user_id`** (str): A unique identifier for the authority.
-   **`authority_name`** (str): The name associated with the authority.

## Post Model

The `Post` model represents a post entity within the application. It includes optional fields for post content, an authority name, user details, and a timestamp, allowing flexibility in data management.

### Post Fields

-   **`post_id`** (str): A unique identifier for the post, generated using `uuid`.
-   **`title`** (Optional[str]): The title of the post (optional).
-   **`description`** (Optional[str]): The content or description of the post (optional).
-   **`image_path`** (Optional[str]): Path to the image associated with the post (optional).
-   **`authority_name`** (str): Name of the authority associated with the post (mandatory).
-   **`user_name`** (Optional[str]): The name of the user who created the post (optional).
-   **`user_id`** (Optional[str]): Unique identifier for the user who created the post (optional).
-   **`time`** (int): Timestamp for when the post was created, defaults to the current time.

### Post Methods

#### `make_empty_post`

```python
@staticmethod
def make_empty_post() -> "Post":
```

Creates an empty `Post` object with default values for each field, with mandatory fields like `authority_name` set to empty strings.

-   **Returns**: `Post` – A `Post` instance with default empty values.

#### `make_empty_post_with_details`

```python
@staticmethod
def make_empty_post_with_details(
    title: str, description: str, image_path: str = ""
) -> "Post":
```

Creates an empty `Post` object but initializes specific fields with provided values (`title`, `description`, `image_path`). Generates a unique `post_id` and sets the `time` field to the current timestamp.

-   **Parameters**:

    -   `title` (str): Title of the post.
    -   `description` (str): Description of the post.
    -   `image_path` (str): Optional image path (default is an empty string).

-   **Returns**: `Post` – A `Post` instance initialized with the specified details.

---
