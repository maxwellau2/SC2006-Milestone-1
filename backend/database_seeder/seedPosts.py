import sqlite3
import uuid
from datetime import datetime

# Define UUIDs for authorities and posts
authority_uuids = [
    uuid.UUID("123e4567-e89b-12d3-a456-426614174034"),
    uuid.UUID("123e4567-e89b-12d3-a456-426614174009"),
    uuid.UUID("123e4567-e89b-12d3-a456-426614174034"),
    uuid.UUID("123e4567-e89b-12d3-a456-426614174042"),
    uuid.UUID("123e4567-e89b-12d3-a456-426614174010"),
]

post_uuids = [
    uuid.UUID("69282e21-e89b-12d3-a456-426614174041"),  # broken bench in park
    uuid.UUID("69282e21-e89b-12d3-a456-426614174042"),  # broken bulb
    uuid.UUID("69282e21-e89b-12d3-a456-426614174043"),  # sinkhole
    uuid.UUID("69282e21-e89b-12d3-a456-426614174044"),  # pipe leakage
    uuid.UUID("69282e21-e89b-12d3-a456-426614174045"),  # broken fire hydrant
]

# Sample data for each post
posts_data = [
    {
        "PostID": str(post_uuids[0]),
        "Title": "Broken Bench in Park",
        "Description": "The damaged bench in the park has been fully repaired and is now safe for public use. Visitors can once again enjoy the park comfortably.",
        "imagePath": f"img/postImages/{str(post_uuids[0])}.png",
        "AuthorityName": "Emergency Services",
        "UserName": "Singapore Civil Defence Force HQ",
        "UserID": str(authority_uuids[0]),
        "time": int(datetime.now().timestamp())
    },
    {
        "PostID": str(post_uuids[1]),
        "Title": "Broken Bulb",
        "Description": "The street light bulb that was broken has been successfully replaced. The area is now well-lit, enhancing safety for pedestrians at night.",
        "imagePath": f"img/postImages/{str(post_uuids[1])}.png",
        "AuthorityName": "Community Center",
        "UserName": "Ang Mo Kio Community Center",
        "UserID": str(authority_uuids[1]),
        "time": int(datetime.now().timestamp()-10)
    },
    {
        "PostID": str(post_uuids[2]),
        "Title": "Sinkhole",
        "Description": "The sinkhole that disrupted traffic on the main road has been filled. Road conditions have been restored, and traffic flow is back to normal.",
        "imagePath": f"img/postImages/{str(post_uuids[2])}.png",
        "AuthorityName": "Emergency Services",
        "UserName": "Singapore Civil Defence Force HQ",
        "UserID": str(authority_uuids[2]),
        "time": int(datetime.now().timestamp()-20)
    },
    {
        "PostID": str(post_uuids[3]),
        "Title": "Pipe Leakage",
        "Description": "The water pipe leakage near the building entrance has been fixed. Water supply and access to the building are now fully restored.",
        "imagePath": f"img/postImages/{str(post_uuids[3])}.png",
        "AuthorityName": "Community Center",
        "UserName": "Ghim Moh Community Center",
        "UserID": str(authority_uuids[3]),
        "time": int(datetime.now().timestamp()-30)
    },
    {
        "PostID": str(post_uuids[4]),
        "Title": "Broken Fire Hydrant",
        "Description": "The damaged fire hydrant has been successfully repaired and is now fully operational, ensuring safety in case of emergencies.",
        "imagePath": f"img/postImages/{str(post_uuids[4])}.png",
        "AuthorityName": "Fire Station",
        "UserName": "Marina Bay Fire Station",
        "UserID": str(authority_uuids[4]),
        "time": int(datetime.now().timestamp()-40)
    },
]


def get_connection_instance(db_name: str = "database/posts.db") -> sqlite3.Connection:
    """Establish a new connection to the database."""
    return sqlite3.connect(db_name)

def seed_posts():
    conn = get_connection_instance()
    insert_query = """
    INSERT INTO Post (PostID, Title, Description, imagePath, AuthorityName, UserName, UserID, time)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """
    try:
        cursor = conn.cursor()
        for post in posts_data:
            cursor.execute(
                insert_query,
                (
                    str(post["PostID"]),
                    post["Title"],
                    post["Description"],
                    post["imagePath"],
                    post["AuthorityName"],
                    post["UserName"],
                    str(post["UserID"]),
                    post["time"],
                ),
            )
        conn.commit()
        print("Posts seeded successfully.")
    except sqlite3.Error as e:
        print(f"Error seeding posts: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    seed_posts()
