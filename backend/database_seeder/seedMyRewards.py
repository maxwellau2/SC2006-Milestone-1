import sqlite3
import time
import uuid
from datetime import datetime, timedelta
import random


# Define the function to generate a random expiry date
def generate_expiry(days=30):
    expiry_date = datetime.now() + timedelta(days=days)
    return int(expiry_date.timestamp())


# Predefined user IDs for seeding rewards
predefined_user_ids = [
    "123e4567-e89b-12d3-a456-426614174000",
    "123e4567-e89b-12d3-a456-426614174001",
    "123e4567-e89b-12d3-a456-426614174002",
    "123e4567-e89b-12d3-a456-426614174003",
    "123e4567-e89b-12d3-a456-426614174004",
    "123e4567-e89b-12d3-a456-426614174005",
    "123e4567-e89b-12d3-a456-426614174006",
]

valid_reward_ids = ["rw123", "rw456", "rw789", "rw012", "rw345", "rw567"]


def generate_gift_code(reward_id: str, user_id: str) -> str:
    # random recipe
    return reward_id + user_id + str(int(time.time()))


# Generate dummy rewards
dummy_rewards = [
    {
        "rewardId": random.choice(valid_reward_ids),
        "userId": user_id,
        "expiry": generate_expiry(random.randint(20, 60)),  # Expiry 20-60 days from now
        "giftcode": generate_gift_code(random.choice(valid_reward_ids), user_id),
    }
    for user_id in predefined_user_ids
]


# Insert dummy rewards into the MyRewards table
def insert_dummy_rewards():
    conn = sqlite3.connect("database/myRewards.db")
    insert_query = """
    INSERT INTO MyRewards (rewardId, userId, expiry, giftcode)
    VALUES (?, ?, ?, ?);
    """

    try:
        cursor = conn.cursor()
        for reward in dummy_rewards:
            cursor.execute(
                insert_query,
                (
                    reward["rewardId"],
                    reward["userId"],
                    reward["expiry"],
                    reward["giftcode"],
                ),
            )
        conn.commit()
        print("MyRewards seed data inserted successfully.")
    except sqlite3.Error as e:
        print(f"Error inserting MyRewards seed data: {e}")
    finally:
        conn.close()


# Run the seed insertion
insert_dummy_rewards()
