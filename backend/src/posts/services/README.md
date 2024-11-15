Here’s the documentation in a `README.md` format to document the `AuthorityService`:

---

# AuthorityService Documentation

The `AuthorityService` is a Python class designed to manage authorities within the `Authority` table of an SQLite database. This service includes methods to create, read, update, and delete authority records. The database schema and each method’s functionality are described below.

## Table of Contents

-   [Overview](#overview)
-   [Database Schema](#database-schema)
-   [Setup Instructions](#setup-instructions)
-   [Methods](#methods)
    -   [get_connection_instance](#get_connection_instance)
    -   [create_authority_table](#create_authority_table)
    -   [create_entry](#create_entry)
    -   [update_entry](#update_entry)
    -   [delete_entry](#delete_entry)
    -   [read_entry](#read_entry)
    -   [read_all_entries](#read_all_entries)
    -   [parse_entry](#parse_entry)

## Overview

`AuthorityService` provides CRUD operations for managing entries in the `Authority` table. The class uses SQLite for database management, with each method handling specific interactions with the database.

## Database Schema

The `Authority` table schema includes the following columns:

-   **UserID** (TEXT, Primary Key): Unique identifier for each authority.
-   **AuthorityName** (TEXT, Not Null): The name of the authority.

## Setup Instructions

1. Ensure SQLite3 is installed on your system.
2. The database file `authority.db` should be in the `database/` directory.
3. The `Authority` model is required and assumed to be located in `src/posts/models/AuthorityModel.py`.

## Methods

### get_connection_instance

```python
@staticmethod
def get_connection_instance() -> sqlite3.Connection:
```

Establishes a new database connection to `authority.db`.

-   **Returns**: `sqlite3.Connection` – a connection object to the `authority.db` SQLite database.

### create_authority_table

```python
@staticmethod
def create_authority_table():
```

Creates the `Authority` table in the database if it does not exist.

-   **Table Columns**:
    -   `UserID`: Primary key, `TEXT`
    -   `AuthorityName`: Not null, `TEXT`

### create_entry

```python
@staticmethod
def create_entry(authority: Authority) -> Tuple[int, Optional[Authority]]:
```

Inserts a new record into the `Authority` table.

-   **Parameters**:

    -   `authority` (Authority): An `Authority` instance containing `user_id` and `authority_name`.

-   **Returns**:
    -   `(201, Authority)`: Record created successfully.
    -   `(400, None)`: Duplicate `user_id`.
    -   `(500, None)`: Internal error.

### update_entry

```python
@staticmethod
def update_entry(user_id: str, new_authority_name: str) -> int:
```

Updates the `AuthorityName` for an existing record based on `user_id`.

-   **Parameters**:

    -   `user_id` (str): Identifier of the authority to update.
    -   `new_authority_name` (str): New authority name.

-   **Returns**:
    -   `200`: Update successful.
    -   `404`: Authority not found.
    -   `500`: Internal error.

### delete_entry

```python
@staticmethod
def delete_entry(user_id: str) -> int:
```

Deletes an authority record from the database by `user_id`.

-   **Parameters**:

    -   `user_id` (str): Identifier of the authority to delete.

-   **Returns**:
    -   `200`: Deletion successful.
    -   `404`: Authority not found.
    -   `500`: Internal error.

### read_entry

```python
@staticmethod
def read_entry(user_id: str) -> Tuple[int, Optional[Authority]]:
```

Fetches an authority record by `user_id`.

-   **Parameters**:

    -   `user_id` (str): Identifier of the authority to fetch.

-   **Returns**:
    -   `(200, Authority)`: Record found.
    -   `(404, None)`: Authority not found.
    -   `(500, None)`: Internal error.

### read_all_entries

```python
@staticmethod
def read_all_entries() -> Tuple[int, List[Authority]]:
```

Fetches all authority records from the `Authority` table.

-   **Returns**:
    -   `(200, List[Authority])`: List of all authorities.
    -   `(500, [])`: Internal error.

### parse_entry

```python
@staticmethod
def parse_entry(result: Tuple) -> Authority:
```

Converts a row from the `Authority` table into an `Authority` instance.

-   **Parameters**:

    -   `result` (Tuple): Row data from the `Authority` table.

-   **Returns**:
    -   `Authority`: An instance of the `Authority` model populated with data from the row.

---

# PostService Documentation

The `PostService` class manages posts in the `Post` table of an SQLite database. It includes methods to create, read, update, and delete posts, as well as helper functions for managing connections and fetching related user and authority information.

## Table of Contents

-   [Overview](#overview)
-   [Database Schema](#database-schema)
-   [Setup Instructions](#setup-instructions)
-   [Methods](#methods)
    -   [get_connection_instance](#get_connection_instance)
    -   [ensure_connection_open](#ensure_connection_open)
    -   [create_entry](#create_entry)
    -   [update_entry](#update_entry)
    -   [delete_entry](#delete_entry)
    -   [read_entry](#read_entry)
    -   [read_all_entries](#read_all_entries)
    -   [parse_entry](#parse_entry)
    -   [get_user_name](#get_user_name)
    -   [create_post_with_authority](#create_post_with_authority)

## Overview

The `PostService` class interacts with an SQLite database (`posts.db`) to manage `Post` records. It includes methods to create, update, delete, and retrieve posts, with features to manage connections and fetch associated data from `AuthorityService` and the `users.db` database.

## Database Schema

The `Post` table schema includes the following columns:

-   **PostID** (TEXT, Primary Key): Unique identifier for each post.
-   **Title** (TEXT): Title of the post.
-   **Description** (TEXT): Description of the post.
-   **imagePath** (TEXT): Path to the post’s image.
-   **AuthorityName** (TEXT): Name of the authority associated with the post.
-   **UserName** (TEXT): Name of the user who created the post.
-   **UserID** (TEXT): Unique identifier of the user who created the post.
-   **time** (INTEGER): Timestamp of when the post was created.

## Setup Instructions

1. Ensure SQLite3 is installed.
2. Place the `posts.db` and `users.db` files in the `database/` directory.
3. The `Post` model should be available in `src/posts/models/PostModel.py`.

## Methods

### get_connection_instance

```python
@staticmethod
def get_connection_instance() -> sqlite3.Connection:
```

Establishes a new connection to `posts.db`.

-   **Returns**: `sqlite3.Connection` – connection to the SQLite database with `row_factory` set to `sqlite3.Row`.

### ensure_connection_open

```python
@staticmethod
def ensure_connection_open(conn: Optional[sqlite3.Connection]) -> sqlite3.Connection:
```

Ensures that the database connection is open, reopening it if necessary.

-   **Parameters**:
    -   `conn` (Optional[sqlite3.Connection]): Existing connection to verify.
-   **Returns**: `sqlite3.Connection` – verified open connection.

### create_entry

```python
@staticmethod
def create_entry(post: Post) -> Tuple[int, Optional[Post]]:
```

Inserts a new record in the `Post` table.

-   **Parameters**:
    -   `post` (Post): A `Post` instance containing data to insert.
-   **Returns**:
    -   `(201, Post)`: Record created successfully.
    -   `(400, None)`: Integrity error, e.g., duplicate `post_id`.
    -   `(500, None)`: Internal server error.

### update_entry

```python
@staticmethod
def update_entry(
    post_id: str,
    new_title: Optional[str] = None,
    new_description: Optional[str] = None,
    new_image_path: Optional[str] = None,
    new_authority_name: Optional[str] = None,
    new_user_id: Optional[str] = None,
) -> int:
```

Updates an existing post's fields based on `post_id`.

-   **Parameters**:
    -   `post_id` (str): Identifier of the post to update.
    -   Additional optional fields (`new_title`, `new_description`, etc.) to specify fields to update.
-   **Returns**:
    -   `200`: Update successful.
    -   `404`: Post not found.
    -   `400`: No fields provided for update.
    -   `500`: Internal server error.

### delete_entry

```python
@staticmethod
def delete_entry(post_id: str) -> int:
```

Deletes a post from the `Post` table by `post_id`.

-   **Parameters**:
    -   `post_id` (str): Identifier of the post to delete.
-   **Returns**:
    -   `200`: Deletion successful.
    -   `404`: Post not found.
    -   `500`: Internal server error.

### read_entry

```python
@staticmethod
def read_entry(post_id: str) -> Tuple[int, Optional[Post]]:
```

Fetches a post by `post_id`.

-   **Parameters**:
    -   `post_id` (str): Identifier of the post to fetch.
-   **Returns**:
    -   `(200, Post)`: Record found.
    -   `(404, None)`: Post not found.
    -   `(500, None)`: Internal server error.

### read_all_entries

```python
@staticmethod
def read_all_entries() -> Tuple[int, List[Post]]:
```

Fetches all posts, ordered by creation time in descending order.

-   **Returns**:
    -   `(200, List[Post])`: List of all posts.
    -   `(500, [])`: Internal server error.

### parse_entry

```python
@staticmethod
def parse_entry(result: Tuple) -> Post:
```

Converts a row from the `Post` table into a `Post` instance.

-   **Parameters**:
    -   `result` (Tuple): Row data from the `Post` table.
-   **Returns**: `Post` – A populated `Post` instance.

### get_user_name

```python
@staticmethod
def get_user_name(user_id: str) -> Optional[str]:
```

Fetches the user name associated with a `user_id` from `users.db`.

-   **Parameters**:
    -   `user_id` (str): Identifier of the user.
-   **Returns**:
    -   `str`: The `UserName` if found.
    -   `None`: User not found or error occurred.

### create_post_with_authority

```python
@staticmethod
def create_post_with_authority(
    user_id: str, post: Post
) -> Tuple[int, Optional[Post]]:
```

Creates a post with additional authority and user name fields fetched from other databases.

-   **Parameters**:
    -   `user_id` (str): ID of the user creating the post.
    -   `post` (Post): Initial `Post` instance containing basic information.
-   **Returns**:
    -   `(201, Post)`: Post created successfully with additional fields.
    -   `(404, None)`: User or authority not found.
    -   `(400, None)`: Integrity error, e.g., duplicate `post_id`.
    -   `(500, None)`: Internal server error.

---
