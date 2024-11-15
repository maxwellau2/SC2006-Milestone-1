# Rewards API Documentation

The `Rewards API` provides endpoints for managing and interacting with reward entities in a database. This API enables CRUD operations, uploading and retrieving reward images, claiming rewards, and checking reward validity.

## Table of Contents

-   [Overview](#overview)
-   [Setup](#setup)
-   [Endpoints](#endpoints)
    -   [Retrieve All Rewards](#retrieve-all-rewards)
    -   [Retrieve Reward by ID](#retrieve-reward-by-id)
    -   [Create a Reward](#create-a-reward)
    -   [Update Reward Quantity](#update-reward-quantity)
    -   [Check Reward Validity](#check-reward-validity)
    -   [Generate Encoded Reward](#generate-encoded-reward)
    -   [Decode Reward](#decode-reward)
    -   [Delete Reward](#delete-reward)
    -   [Wipe All Rewards](#wipe-all-rewards)
    -   [Retrieve Reward Image](#retrieve-reward-image)
    -   [Upload Reward Image](#upload-reward-image)
    -   [Retrieve User Rewards](#retrieve-user-rewards)
    -   [Claim Reward](#claim-reward)
    -   [Update Reward](#update-reward)

## Overview

The `Rewards API` enables the management of rewards within a system, allowing for creation, updating, claiming, and retrieval of rewards, including image uploads. This API is implemented using FastAPI.

## Setup

1. Ensure a SQLite database named `rewards.db` is in place.
2. Store reward images in the `img/voucherimg` directory.
3. Ensure all dependencies are installed:
    ```bash
    pip install fastapi pydantic sqlite3 pillow
    ```

## Endpoints

### Retrieve All Rewards

-   **GET** `/rewards/all`
-   **Description**: Retrieves a list of all rewards.
-   **Response**: List of `Reward` objects.

### Retrieve Reward by ID

-   **GET** `/rewards/{reward_id}`
-   **Description**: Retrieves a reward by its unique identifier.
-   **Response**: A `Reward` object if found.

### Create a Reward

-   **POST** `/rewards/`
-   **Description**: Creates a new reward with an optional image.
-   **Request Parameters**:
    -   `description` (str): Description of the reward.
    -   `pointsRequired` (int): Points required to claim.
    -   `availability` (int): Number of rewards available.
    -   `validity` (Optional[int]): Expiration timestamp (default: 0).
    -   `file` (UploadFile): Image file for the reward.
-   **Response**: The newly created `Reward` object.

### Update Reward Quantity

-   **PUT** `/rewards/{reward_id}/quantity`
-   **Description**: Updates the quantity of a reward.
-   **Request Parameters**:
    -   `reward_id` (str): Reward ID.
    -   `quantity` (int): New quantity.
-   **Response**: Success message if updated.

### Check Reward Validity

-   **GET** `/rewards/{reward_id}/validity`
-   **Description**: Checks if a reward is still valid.
-   **Response**: `{ "is_valid": true/false }`

### Generate Encoded Reward

-   **POST** `/rewards/{reward_id}/generate`
-   **Description**: Generates a Base64-encoded string for the reward with a specified duration.
-   **Request Parameters**:
    -   `duration` (int): Validity duration in days.
-   **Response**: Encoded reward string.

### Decode Reward

-   **POST** `/rewards/decode`
-   **Description**: Decodes a Base64-encoded reward string.
-   **Request Parameters**:
    -   `encoded_recipe` (str): Encoded reward string.
-   **Response**: Decoded reward string.

### Delete Reward

-   **DELETE** `/rewards/{reward_id}`
-   **Description**: Deletes a reward by its ID.
-   **Response**: Success message if deleted.

### Wipe All Rewards

-   **DELETE** `/rewards/wipe`
-   **Description**: Deletes all rewards from the database.
-   **Response**: Success message if wiped.

### Retrieve Reward Image

-   **GET** `/rewards/{reward_identifier}/image`
-   **Description**: Retrieves the image associated with the reward ID.
-   **Response**: Image file if found, or a default image if not.

### Upload Reward Image

-   **POST** `/rewards/{reward_identifier}/image`
-   **Description**: Uploads an image for the reward.
-   **Request Parameters**:
    -   `file` (UploadFile): Image file to associate with the reward.
-   **Response**: Success message with file path.

### Retrieve User Rewards

-   **GET** `/rewards/myrewards/{user_id}`
-   **Description**: Retrieves all rewards claimed by a user.
-   **Response**: List of user rewards.

### Claim Reward

-   **POST** `/rewards/claim/{reward_id}`
-   **Description**: Claims a reward for the user.
-   **Request Parameters**:
    -   `reward_id` (str): Reward ID.
    -   `user_id` (str): User ID.
-   **Response**: Success message if claimed or error if insufficient points.

### Update Reward

-   **PUT** `/rewards/update/{reward_id}`
-   **Description**: Updates the attributes of a reward.
-   **Request Parameters**:
    -   `reward_id` (str): Reward ID.
    -   `reward` (RewardUpdate): Attributes to update.
-   **Response**: Success message if updated.
