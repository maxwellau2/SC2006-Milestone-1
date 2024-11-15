import uuid
import base64
from datetime import datetime, timedelta
import sqlite3


class Reward:
    def __init__(
        self,
        description: str,
        pointsRequired: int,
        availability: int,
        validity: int = 0,
        rewardID: str = None,
    ):
        self.rewardID: str = rewardID if rewardID else uuid.uuid4()
        self.description: str = description
        self.pointsRequired: int = pointsRequired  # Uint16 in the diagram
        self.validity: int = validity  # Uint16 in the diagram
        self.availability: int = (
            availability  # Uint16 in the diagram, count of redeemable items
        )

    def generateReward(self, duration: int) -> str:
        """
        Generates a Base64-encoded recipe string based on the reward description and expiration timestamp.

        :param duration: Duration in days until expiration.
        :return: A Base64-encoded string representing the reward with expiration timestamp.
        """
        # Calculate expiration timestamp
        expiration_time = datetime.now() + timedelta(days=duration)
        expire_timestamp = int(expiration_time.timestamp())
        self.validity = expire_timestamp

        # Create recipe string combining description and expiration timestamp
        recipe = f"{self.description}+{expire_timestamp}"

        # Encode the recipe string in Base64
        encoded_recipe = base64.b64encode(recipe.encode()).decode()
        return encoded_recipe

    def decodeReward(self, encoded_recipe: str) -> str:
        """
        Decodes a Base64-encoded reward back to its original form.

        :param encoded_recipe: Base64-encoded reward string.
        :return: Decoded original reward string.
        """
        decoded_recipe = base64.b64decode(encoded_recipe).decode()
        return decoded_recipe

    def getValidity(self) -> bool:
        """
        Checks if the reward is still valid based on its validity period.
        :return: True if valid, False otherwise.
        """
        return self.validity > 0

    def getPointsRequired(self) -> int:
        """
        Returns the number of points required to redeem the reward.
        :return: Points required for redemption.
        """
        return self.pointsRequired

    def getAvailability(self) -> int:
        """
        Returns the number of redeemable items remaining.
        :return: Available reward count.
        """
        return self.availability

    def __repr__(self) -> str:
        return (
            f"Reward(rewardID={self.rewardID}, description={self.description}, pointsRequired={self.pointsRequired}, "
            f"validity={self.validity}, availability={self.availability})"
        )


# if __name__ == "__main__":
#     # Create a Reward object
#     reward = Reward("RW123", "GRABVOUCHER5$", 100, 30, 50)

#     # Test: Generate a Base64-encoded reward string
#     duration = 3
#     encoded_reward = reward.generateReward(duration)
#     print(f"Encoded Reward: {encoded_reward}")

#     # Expected output: R1JBQlZPVUNIRVI1JCsxMjM5ODEyMw==

#     # Test: Decode the Base64-encoded reward string
#     decoded_reward = reward.decodeReward(encoded_reward)
#     print(f"Decoded Reward: {decoded_reward}")

#     # split the decoded by +
#     r = decoded_reward.split("+")
#     # convert the timestamp into day to see
#     dt_object = datetime.fromtimestamp(int(r[1]))

#     # Format the datetime object to 'yyyy-mm-dd'
#     formatted_date = dt_object.strftime("%Y-%m-%d")
#     print(formatted_date)

#     # Expected output: GRABVOUCHER5$+12398123

#     # Test: Get validity of the reward
#     is_valid = reward.getValidity()
#     print(f"Is Reward Valid? {is_valid}")

#     # Expected output: True (since the validity is set to 30)

#     # Test: Get the points required to redeem the reward
#     points_required = reward.getPointsRequired()
#     print(f"Points Required: {points_required}")

#     # Expected output: 100

#     # Test: Get the availability of the reward
#     availability = reward.getAvailability()
#     print(f"Availability: {availability}")

#     # Expected output: 50

#     # Output the full Reward object
#     print(reward)

#     # Expected output:
#     # Reward(rewardID=RW123, description=GRABVOUCHER5$, pointsRequired=100, validity=30, availability=50, userID=<userID>)

# Establish database connection
conn = sqlite3.connect("database/rewards.db")


def create_reward(reward: Reward) -> None:
    """Insert a new reward into the Reward table."""
    insert_query = """
    INSERT INTO Reward (RewardID, Description, PointsRequired, Validity, Availability)
    VALUES (?, ?, ?, ?, ?);
    """
    try:
        cursor = conn.cursor()
        cursor.execute(
            insert_query,
            (
                str(reward.rewardID),
                reward.description,
                reward.pointsRequired,
                reward.validity,
                reward.availability,
            ),
        )
        conn.commit()
    except sqlite3.IntegrityError as e:
        print(e)
    except sqlite3.Error as e:
        print(f"Error inserting reward: {e}")


# Dummy reward data
dummy_rewards = [
    Reward(
        rewardID="rw123",
        description="Grab-10",
        pointsRequired=40,
        validity=30,
        availability=50,
    ),
    Reward(
        rewardID="rw456", description="Starbucks-5", pointsRequired=250, availability=30
    ),
    Reward(
        rewardID="rw789",
        description="FoodPanda-15",
        pointsRequired=300,
        availability=40,
    ),
    Reward(
        rewardID="rw012",
        description="FairPrice-20",
        pointsRequired=500,
        availability=20,
    ),
    Reward(
        rewardID="rw345", description="Grab-20", pointsRequired=1000, availability=100
    ),
    Reward(
        rewardID="rw567", description="Luckin-5", pointsRequired=600, availability=10
    ),
]

# Insert each dummy reward into the database
for reward in dummy_rewards:
    reward.generateReward(5)
    create_reward(reward)

conn.close()
