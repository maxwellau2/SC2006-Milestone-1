# RewardService.py
import sqlite3
import time
from typing import List, Optional, Tuple
from src.rewards.models.MyRewards import MyRewards
from src.rewards.models.RewardModel import Reward, RewardUpdate
import uuid


class RewardService:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def create_reward_table(self):
        create_table_query = """
        CREATE TABLE IF NOT EXISTS Reward (
            RewardID TEXT PRIMARY KEY,
            Description TEXT NOT NULL,
            PointsRequired INTEGER NOT NULL,
            Validity INTEGER,
            Availability INTEGER NOT NULL
        );
        """
        cursor = self.conn.cursor()
        cursor.execute(create_table_query)
        self.conn.commit()

    def create_reward(self, reward: Reward) -> int:
        insert_query = """
        INSERT INTO Reward (RewardID, Description, PointsRequired, Validity, Availability)
        VALUES (?, ?, ?, ?, ?);
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                insert_query,
                (
                    reward.rewardID,
                    reward.description,
                    reward.pointsRequired,
                    reward.validity,
                    reward.availability,
                ),
            )
            self.conn.commit()
            return 201  # Created
        except sqlite3.IntegrityError:
            return 400  # RewardID already exists
        except sqlite3.Error as e:
            print(f"Error inserting reward: {e}")
            return 500  # Internal Server Error

    def read_all_rewards(self) -> Tuple[int, List[Reward]]:
        select_query = "SELECT * FROM Reward;"
        cursor = self.conn.cursor()
        cursor.execute(select_query)
        results = cursor.fetchall()

        rewards = [
            Reward(
                rewardID=result[0],
                description=result[1],
                pointsRequired=result[2],
                validity=result[3],
                availability=result[4],
            )
            for result in results
        ]
        return 200, rewards

    def update_reward(self, reward_id: str, reward: RewardUpdate) -> int:
        query = "UPDATE Reward SET description = ?, pointsRequired = ?, validity = ?, availability = ? WHERE rewardId = ?;"
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                query,
                (
                    reward.description,
                    reward.pointsRequired,
                    reward.validity,
                    reward.availability,
                    reward_id,
                ),
            )
            self.conn.commit()
            print(self.read_all_rewards())
            print("done")
            return 200
        except sqlite3.Error as e:
            print(e)
            return 400

    def get_user_rewards(self, user_id: str) -> List[MyRewards]:
        conn = sqlite3.connect("database/myRewards.db")
        query = (
            "SELECT rewardId, userId, expiry, giftcode FROM MyRewards WHERE userId = ?;"
        )
        rewards = []

        try:
            cursor = conn.cursor()
            cursor.execute(query, (user_id,))
            rows = cursor.fetchall()

            for row in rows:
                reward = MyRewards(
                    reward_id=row[0],
                    user_id=row[1],
                    expiry=row[2],  # Convert Unix timestamp to datetime
                    giftcode=row[3],
                )
                rewards.append(reward)

        except sqlite3.Error as e:
            print(f"Error retrieving rewards: {e}")
        finally:
            conn.close()
        return 200, rewards

    def claim_reward_by_id(
        self, reward_id: str, user_id: str
    ) -> Tuple[int, Optional[Reward]]:
        # lookup the reward
        res = self.read_reward_by_id(reward_id)
        if res[1] == None:  # not found
            return 404, None
        reward: Reward = res[1]
        current_timestamp = int(time.time())
        one_year_later_timestamp = current_timestamp + (365 * 24 * 60 * 60)
        reward.validity = one_year_later_timestamp
        # look up the cost
        cost = reward.pointsRequired
        # lookup points in user DB
        conn_user = sqlite3.connect("database/users.db")
        cursor = conn_user.cursor()
        cursor.execute("SELECT points FROM User WHERE userID = ?;", (user_id,))
        points = cursor.fetchone()
        if points is None:
            return 404, None
        points = points[0]
        if points < cost:
            return 403, None
        print("hello")
        # update the points in user DB
        update_query = "UPDATE User SET points = points - ? WHERE userID = ?;"
        cursor = conn_user.cursor()
        cursor.execute(update_query, (cost, user_id))
        conn_user.commit()
        # create the MyRewards entry
        conn_myrewards = sqlite3.connect("database/myRewards.db")

        insert_query = "INSERT INTO MyRewards (RewardID, UserID, Expiry, Giftcode) VALUES (?, ?, ?, ?);"
        cursor = conn_myrewards.cursor()
        cursor.execute(
            insert_query,
            (
                reward.rewardID,
                user_id,
                reward.validity,
                self.generate_gift_code(reward.rewardID, user_id),
            ),
        )
        conn_myrewards.commit()

        # close the connections
        conn_user.close()
        conn_myrewards.close()
        return 200, reward

    def generate_gift_code(self, reward_id: str, user_id: str) -> str:
        # random recipe
        return reward_id + user_id + str(int(time.time()))

    def is_valid_uuid(self, val):
        try:
            uuid.UUID(str(val))
            return True
        except ValueError:
            return False

    def read_reward_by_id(self, reward_id: str) -> Tuple[int, Optional[Reward]]:
        select_query = "SELECT * FROM Reward WHERE RewardID = ?;"
        cursor = self.conn.cursor()
        cursor.execute(select_query, (reward_id,))
        result = cursor.fetchone()
        if result:
            reward = Reward(
                rewardID=result[0],
                description=result[1],
                pointsRequired=result[2],
                validity=result[3],
                availability=result[4],
            )
            return 200, reward
        else:
            return 404, None  # Not Found

    def read_reward_by_name(self, name: str) -> Tuple[int, Optional[Reward]]:
        select_query = "SELECT * FROM Reward WHERE Description = ?;"
        cursor = self.conn.cursor()
        cursor.execute(select_query, (name,))
        result = cursor.fetchone()
        if result:
            reward = Reward(
                rewardID=result[0],
                description=result[1],
                pointsRequired=result[2],
                validity=result[3],
                availability=result[4],
            )
            return 200, reward
        else:
            return 404, None  # Not Found

    def update_reward_availability(self, reward_id: str, availability: int) -> int:
        update_query = "UPDATE Reward SET Availability = ? WHERE RewardID = ?;"
        cursor = self.conn.cursor()
        cursor.execute(update_query, (availability, reward_id))
        self.conn.commit()
        return 200 if cursor.rowcount > 0 else 404

    def delete_reward(self, reward_id: str) -> int:
        delete_query = "DELETE FROM Reward WHERE RewardID = ?;"
        cursor = self.conn.cursor()
        cursor.execute(delete_query, (reward_id,))
        self.conn.commit()
        return 200 if cursor.rowcount > 0 else 404

    def close_connection(self):
        if self.conn:
            self.conn.close()
            print("Database connection closed.")
