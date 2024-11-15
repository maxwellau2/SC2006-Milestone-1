import sqlite3


if __name__ == "__main__":
    # Connect to the user database 'users.db' to fetch data from 'seedUser'
    conn_user = sqlite3.connect("database/users.db")
    cursor_user = conn_user.cursor()

    # Connect to the new SQLite database 'Authority.db'
    conn_authority = sqlite3.connect("database/authority.db")
    cursor_authority = conn_authority.cursor()

    # Dictionary of authority types by userName for reference
    authority_types = {
        "amogh1": "Strip Club",
        "maxwell1": "Police Station",
        "Bukit Batok Fire Station": "Fire Station",
        "Tampines Police Division": "Police Station",
        "Ang Mo Kio Community Center": "Community Center",
        "Marina Bay Fire Station": "Fire Station",
        "Woodlands Police Division": "Police Station",
        "Bedok Community Center": "Community Center",
        "Jurong Fire Station": "Fire Station",
        "Choa Chu Kang Police Post": "Police Station",
        "Pasir Ris Community Center": "Community Center",
        "Clementi Fire Station": "Fire Station",
        "Hougang Neighbourhood Police": "Police Station",
        "Yishun Community Center": "Community Center",
        "Geylang Fire Station": "Fire Station",
        "Kreta Ayer Police Post": "Police Station",
        "Bukit Merah Community Center": "Community Center",
        "Serangoon Fire Station": "Fire Station",
        "Sengkang Neighbourhood Police": "Police Station",
        "Bukit Panjang Community Center": "Community Center",
        "Paya Lebar Fire Post": "Fire Station",
        "Queenstown Neighbourhood Police": "Police Station",
        "Toa Payoh Central Community Center": "Community Center",
        "Tan Tock Seng Hospital": "Hospital",
        "Singapore General Hospital": "Hospital",
        "Khoo Teck Puat Hospital": "Hospital",
        "Changi General Hospital": "Hospital",
        "Mount Elizabeth Hospital": "Hospital",
        "KK Women's and Children's Hospital": "Hospital",
        "Singapore Civil Defence Force HQ": "Emergency Services",
        "Police Cantonment Complex": "Police Station",
        "Clementi Neighbourhood Police Centre": "Police Station",
        "Eunos Fire Station": "Fire Station",
        "Bukit Timah Community Club": "Community Center",
        "Jurong West Police Division": "Police Station",
        "Toa Payoh Fire Station": "Fire Station",
        "Potong Pasir Community Center": "Community Center",
        "Ghim Moh Community Center": "Community Center",
        "Yew Tee Neighbourhood Police": "Police Station",
        "Kallang Fire Station": "Fire Station",
        "Tanglin Neighbourhood Police": "Police Station",
        "Sembawang Community Center": "Community Center",
        "Nanyang Community Center": "Community Center",
        "Orchard Neighbourhood Police": "Police Station",
        "Cairnhill Community Center": "Community Center",
        "Sentosa Fire Station": "Fire Station",
        "Outram Community Center": "Community Center",
        "Harbourfront Fire Post": "Fire Station",
        "Chinatown Neighbourhood Police": "Police Station",
        "Marine Parade Community Center": "Community Center",
        "Newton Police Division": "Police Station",
        "Kovan Fire Station": "Fire Station",
        "MacPherson Neighbourhood Police": "Police Station",
    }

    # Step 1: Create the new table 'authority' with two columns: userID and authorityName
    cursor_authority.execute(
        """
        CREATE TABLE IF NOT EXISTS authority (
            userID TEXT PRIMARY KEY,
            authorityName TEXT
        )
    """
    )

    # Step 2: Insert authority users from 'seedUser' into 'authority' table
    # Here we join the 'authority_types' dictionary with the user data based on userName
    cursor_user.execute(
        """
                    SELECT * from User;
                        """
    )

    cursor_user.execute(
        """
        SELECT userID, userName FROM User WHERE isAuthority = 1
        """
    )

    # Fetch all authority users from the 'seedUser' table
    authority_users = cursor_user.fetchall()

    # Debugging step: Check the fetched authority users
    print(f"Fetched {len(authority_users)} users from 'seedUser' table.")

    # Insert the authority users into 'authority' table with their authority type
    for user in authority_users:
        user_id, user_name = user
        authority_type = authority_types.get(user_name, "Unknown")

        # Debugging step: Check user info
        print(
            f"Inserting user: userID={user_id}, userName={user_name}, authorityName={authority_type}"
        )

        # Insert into authority table
        cursor_authority.execute(
            """
            INSERT OR REPLACE INTO authority (userID, authorityName)
            VALUES (?, ?)
            """,
            (user_id, authority_type),
        )

    # Step 3: Commit the transaction to save changes
    conn_authority.commit()

    # Debugging step: Confirm changes were committed
    print("Changes committed to 'authority'.")

    # Close both database connections
    conn_user.close()
    conn_authority.close()
