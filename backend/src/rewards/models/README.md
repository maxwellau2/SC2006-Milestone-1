# Reward Model Documentation

The `Reward` and `RewardUpdate` models represent a reward system, where each reward has an ID, description, point requirements, validity, and availability. The `Reward` model also includes methods for encoding and decoding rewards, as well as checking their validity.

## Table of Contents

-   [Overview](#overview)
-   [RewardUpdate Class](#rewardupdate-class)
    -   [Attributes](#attributes)
-   [Reward Class](#reward-class)
    -   [Attributes](#attributes-1)
    -   [Methods](#methods)
        -   [generateReward](#generatereward)
        -   [decodeReward](#decodereward)
        -   [is_valid](#is_valid)

## Overview

The `Reward` class is designed to manage individual rewards, including generating and validating rewards with an expiration timestamp. The `RewardUpdate` class is a lightweight version meant for updates, ensuring point requirements, validity, and availability are all positive integers.

## RewardUpdate Class

### Attributes

-   **description** (`str`): Description of the reward.
-   **pointsRequired** (`int`): Points required to claim the reward (must be positive).
-   **validity** (`int`): Unix timestamp indicating when the reward expires (non-negative).
-   **availability** (`int`): The number of rewards available (non-negative).

## Reward Class

### Attributes

-   **rewardID** (`str`): Unique identifier for each reward, generated automatically.
-   **description** (`str`): Description of the reward.
-   **pointsRequired** (`int`): Points required to claim the reward (must be positive).
-   **validity** (`int`): Unix timestamp for when the reward expires (non-negative).
-   **availability** (`int`): Number of times the reward can be claimed (non-negative).

### Methods

#### generateReward

```python
def generateReward(self, duration: int) -> str
```

Generates a Base64-encoded reward string that includes an expiration timestamp.

-   **Parameters**:
    -   `duration` (`int`): Duration in days for which the reward is valid.
-   **Returns**: `str` – A Base64-encoded string containing the reward description and expiration timestamp.

#### decodeReward

```python
def decodeReward(self, encoded_recipe: str) -> str
```

Decodes a Base64-encoded reward string back to its original form.

-   **Parameters**:
    -   `encoded_recipe` (`str`): The encoded reward string.
-   **Returns**: `str` – The original decoded string, including the description and expiration timestamp.

#### is_valid

```python
def is_valid(self) -> bool
```

Checks if the reward is still valid by comparing the current timestamp to the reward’s expiration timestamp.

-   **Returns**: `bool` – True if the reward is still valid, False otherwise.

---
