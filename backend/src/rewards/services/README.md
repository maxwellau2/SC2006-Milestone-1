# RewardService Documentation

The `RewardService` class provides functionality to manage reward operations within a SQLite database. It supports CRUD operations for rewards, updating user points, handling reward claims, and managing user-specific rewards.

## Table of Contents

-   [Setup Instructions](#setup-instructions)
-   [Database Schema](#database-schema)
    -   [Reward Table](#reward-table)
    -   [MyRewards Table](#myrewards-table)
-   [Methods](#methods)
    -   [create_reward_table](#create_reward_table)
    -   [create_reward](#create_reward)
    -   [read_all_rewards](#read_all_rewards)
    -   [update_reward](#update_reward)
    -   [get_user_rewards](#get_user_rewards)
    -   [claim_reward_by_id](#claim_reward_by_id)
    -   [generate_gift_code](#generate_gift_code)
    -   [is_valid_uuid](#is_valid_uuid)
    -   [read_reward_by_id](#read_reward_by_id)
    -   [read_reward_by_name](#read_reward_by_name)
    -   [update_reward_availability](#update_reward_availability)
    -   [delete_reward](#delete_reward)
    -   [close_connection](#close_connection)

## Setup Instructions

1. Install SQLite3 to manage database connections and queries.
2. Place the `myRewards.db` and `users.db` files in the `database/` directory for managing user rewards and user data.
3. Import the `RewardService` class and initialize it with a valid database connection.

## Database Schema

### Reward Table

The `Reward` table schema includes the following columns:

-   **RewardID** (TEXT, Primary Key): Unique identifier for each reward.
-   **Description** (TEXT, Not Null): Description of the reward.
-   **PointsRequired** (INTEGER, Not Null): Points needed to claim the reward.
-   **Validity** (INTEGER, Optional): Unix timestamp representing the reward's expiration.
-   **Availability** (INTEGER, Not Null): Number of times the reward can be claimed.

### MyRewards Table

The `MyRewards` table schema includes the following columns:

-   **RewardID** (TEXT): Unique identifier for the reward.
-   **UserID** (TEXT): Identifier of the user claiming the reward.
-   **Expiry** (INTEGER): Unix timestamp representing when the reward expires.
-   **Giftcode** (TEXT): Unique code generated when a reward is claimed.

## Methods

### create_reward_table

```python
def create_reward_table(self)
```

Creates the `Reward` table in the database if it doesn't exist.

-   **Returns**: None

### create_reward

```python
def create_reward(self, reward: Reward) -> int
```

Inserts a new reward into the `Reward` table.

-   **Parameters**:
    -   `reward` (Reward): An instance of `Reward` containing reward details.
-   **Returns**:
    -   `201`: Reward created successfully.
    -   `400`: RewardID already exists.
    -   `500`: Internal server error.

### read_all_rewards

```python
def read_all_rewards(self) -> Tuple[int, List[Reward]]
```

Retrieves all rewards from the `Reward` table.

-   **Returns**: `(200, List[Reward])` if successful.

### update_reward

```python
def update_reward(self, reward_id: str, reward: RewardUpdate) -> int
```

Updates a reward's details in the `Reward` table based on `reward_id`.

-   **Parameters**:
    -   `reward_id` (str): Unique identifier for the reward.
    -   `reward` (RewardUpdate): Contains updated reward information.
-   **Returns**:
    -   `200`: Update successful.
    -   `400`: Internal server error.

### get_user_rewards

```python
def get_user_rewards(self, user_id: str) -> Tuple[int, List[MyRewards]]
```

Retrieves all rewards claimed by a specific user.

-   **Parameters**:
    -   `user_id` (str): Identifier of the user.
-   **Returns**: `(200, List[MyRewards])` if successful.

### claim_reward_by_id

```python
def claim_reward_by_id(self, reward_id: str, user_id: str) -> Tuple[int, Optional[Reward]]
```

Allows a user to claim a reward by checking points and availability.

-   **Parameters**:
    -   `reward_id` (str): Unique identifier for the reward.
    -   `user_id` (str): Identifier of the user claiming the reward.
-   **Returns**:
    -   `(200, Reward)`: Reward claimed successfully.
    -   `(404, None)`: Reward or user not found.
    -   `(403, None)`: Insufficient points.

### generate_gift_code

```python
def generate_gift_code(self, reward_id: str, user_id: str) -> str
```

Generates a unique gift code for the reward claim.

-   **Parameters**:
    -   `reward_id` (str): Reward identifier.
    -   `user_id` (str): User identifier.
-   **Returns**: `str` – Unique gift code.

### is_valid_uuid

```python
def is_valid_uuid(self, val) -> bool
```

Validates if a given value is a valid UUID.

-   **Parameters**:
    -   `val`: Value to validate.
-   **Returns**: `bool` – True if valid UUID, False otherwise.

### read_reward_by_id

```python
def read_reward_by_id(self, reward_id: str) -> Tuple[int, Optional[Reward]]
```

Retrieves a reward by its unique `RewardID`.

-   **Parameters**:
    -   `reward_id` (str): Unique identifier for the reward.
-   **Returns**:
    -   `(200, Reward)`: Reward found.
    -   `(404, None)`: Reward not found.

### read_reward_by_name

```python
def read_reward_by_name(self, name: str) -> Tuple[int, Optional[Reward]]
```

Searches for a reward by its description.

-   **Parameters**:
    -   `name` (str): Description to search for.
-   **Returns**:
    -   `(200, Reward)`: Reward found.
    -   `(404, None)`: Reward not found.

### update_reward_availability

```python
def update_reward_availability(self, reward_id: str, availability: int) -> int
```

Updates the availability count for a specific reward.

-   **Parameters**:
    -   `reward_id` (str): Unique identifier for the reward.
    -   `availability` (int): New availability count.
-   **Returns**: `200` if successful, `404` if reward not found.

### delete_reward

```python
def delete_reward(self, reward_id: str) -> int
```

Deletes a reward by its unique `RewardID`.

-   **Parameters**:
    -   `reward_id` (str): Unique identifier for the reward.
-   **Returns**: `200` if deletion successful, `404` if reward not found.

### close_connection

```python
def close_connection(self)
```

Closes the database connection.

-   **Returns**: None

---
