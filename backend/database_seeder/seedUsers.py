from typing import Literal
import uuid
import sqlite3


class User:
    def __init__(
        self,
        userName: str,
        passwordHash: str,
        emailAddress: str,
        loginStatus: bool,
        points: int,
        notificationPreference: Literal["email", "sms", "push"],
        notificationEnabled: bool,
        isAuthority: bool,
        isModerator: bool,
        userID: uuid.UUID = None,
    ):
        self.userID: uuid.UUID = userID if userID else uuid.uuid4()
        self.userName: str = userName
        self.passwordHash: str = passwordHash
        self.emailAddress: str = emailAddress
        self.loginStatus: bool = loginStatus
        self.points: int = points
        self.notificationPreference: Literal["email", "sms", "push"] = (
            notificationPreference
        )
        self.notificationEnabled: bool = notificationEnabled
        self.isAuthority: bool = isAuthority
        self.isModerator: bool = isModerator

    def __repr__(self) -> str:
        return (
            f"User(userID={self.userID}, userName={self.userName}, email={self.emailAddress}, "
            f"loginStatus={self.loginStatus}, points={self.points}, "
            f"notificationEnabled={self.notificationEnabled}, isAuthority={self.isAuthority}, "
            f"isModerator={self.isModerator})"
        )


conn = sqlite3.connect("database/users.db")


def create_user(user: User) -> None:
    """Insert a new user into the User table."""
    insert_query = """
    INSERT INTO User (userID, userName, passwordHash, emailAddress, loginStatus, points,
                      notificationPreference, notificationEnabled, isAuthority, isModerator)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """
    try:
        cursor = conn.cursor()
        cursor.execute(
            insert_query,
            (
                str(user.userID),
                user.userName,
                user.passwordHash,
                user.emailAddress,
                user.loginStatus,
                user.points,
                user.notificationPreference,
                user.notificationEnabled,
                user.isAuthority,
                user.isModerator,
            ),
        )
        conn.commit()
    except sqlite3.IntegrityError as e:
        print(e)
        return 400, None  # Bad request: userID already exists
    except sqlite3.Error as e:
        print(f"Error inserting user: {e}")
        return 500, None  # Internal server error


from argon2 import PasswordHasher

# Initialize the Argon2 PasswordHasher
ph = PasswordHasher()

# Dummy users based on the image members
# Predefined UUIDs for reproducible seeding
predefined_uuids = [
    uuid.UUID("123e4567-e89b-12d3-a456-426614174000"),
    uuid.UUID("123e4567-e89b-12d3-a456-426614174001"),
    uuid.UUID("123e4567-e89b-12d3-a456-426614174002"),
    uuid.UUID("123e4567-e89b-12d3-a456-426614174003"),
    uuid.UUID("123e4567-e89b-12d3-a456-426614174004"),
    uuid.UUID("123e4567-e89b-12d3-a456-426614174005"),
    uuid.UUID("123e4567-e89b-12d3-a456-426614174006"),
    uuid.UUID("123e4567-e89b-12d3-a456-426614174007"),
    uuid.UUID("123e4567-e89b-12d3-a456-426614174008"),
    uuid.UUID("123e4567-e89b-12d3-a456-426614174009"),
    uuid.UUID("123e4567-e89b-12d3-a456-426614174010"),
    uuid.UUID("123e4567-e89b-12d3-a456-426614174011"),
    uuid.UUID("123e4567-e89b-12d3-a456-426614174012"),
    uuid.UUID("123e4567-e89b-12d3-a456-426614174013"),
    uuid.UUID("123e4567-e89b-12d3-a456-426614174014"),
    uuid.UUID("123e4567-e89b-12d3-a456-426614174015"),
    uuid.UUID("123e4567-e89b-12d3-a456-426614174016"),
    uuid.UUID("123e4567-e89b-12d3-a456-426614174017"),
    uuid.UUID("123e4567-e89b-12d3-a456-426614174018"),
    uuid.UUID("123e4567-e89b-12d3-a456-426614174019"),
    uuid.UUID("123e4567-e89b-12d3-a456-426614174020"),
    uuid.UUID("123e4567-e89b-12d3-a456-426614174021"),
    uuid.UUID("123e4567-e89b-12d3-a456-426614174022"),
    uuid.UUID("123e4567-e89b-12d3-a456-426614174023"),
    uuid.UUID("123e4567-e89b-12d3-a456-426614174024"),
    uuid.UUID("123e4567-e89b-12d3-a456-426614174025"),
    uuid.UUID("123e4567-e89b-12d3-a456-426614174026"),
    uuid.UUID("123e4567-e89b-12d3-a456-426614174027"),
    uuid.UUID("123e4567-e89b-12d3-a456-426614174028"),
    uuid.UUID("123e4567-e89b-12d3-a456-426614174029"),
    uuid.UUID("123e4567-e89b-12d3-a456-426614174030"),
    uuid.UUID("123e4567-e89b-12d3-a456-426614174031"),
    uuid.UUID("123e4567-e89b-12d3-a456-426614174032"),
    uuid.UUID("123e4567-e89b-12d3-a456-426614174033"),
    uuid.UUID("123e4567-e89b-12d3-a456-426614174034"),
    uuid.UUID("123e4567-e89b-12d3-a456-426614174035"),
    uuid.UUID("123e4567-e89b-12d3-a456-426614174036"),
    uuid.UUID("123e4567-e89b-12d3-a456-426614174037"),
    uuid.UUID("123e4567-e89b-12d3-a456-426614174038"),
    uuid.UUID("123e4567-e89b-12d3-a456-426614174039"),
    uuid.UUID("123e4567-e89b-12d3-a456-426614174040"),
    uuid.UUID("123e4567-e89b-12d3-a456-426614174041"),
    uuid.UUID("123e4567-e89b-12d3-a456-426614174042"),
    uuid.UUID("123e4567-e89b-12d3-a456-426614174043"),
    uuid.UUID("123e4567-e89b-12d3-a456-426614174044"),
    uuid.UUID("123e4567-e89b-12d3-a456-426614174045"),
    uuid.UUID("123e4567-e89b-12d3-a456-426614174046"),
    uuid.UUID("123e4567-e89b-12d3-a456-426614174047"),
    uuid.UUID("123e4567-e89b-12d3-a456-426614174048"),
    uuid.UUID("123e4567-e89b-12d3-a456-426614174049"),
    uuid.UUID("123e4567-e89b-12d3-a456-426614174050"),
    uuid.UUID("123e4567-e89b-12d3-a456-426614174051"),
    uuid.UUID("123e4567-e89b-12d3-a456-426614174052"),
    uuid.UUID("123e4567-e89b-12d3-a456-426614174053"),
    uuid.UUID("123e4567-e89b-12d3-a456-426614174054"),
    uuid.UUID("123e4567-e89b-12d3-a456-426614174055"),
    uuid.UUID("123e4567-e89b-12d3-a456-426614174056"),
    uuid.UUID("123e4567-e89b-12d3-a456-426614174057"),
]

# Dummy users with explicit UUIDs for reproducibility
dummy_users = [
    User(
        userName="jingxiang1",
        passwordHash=ph.hash("password1"),
        emailAddress="kehjingxiang@yahoo.com",
        loginStatus=False,
        points=100,
        notificationPreference="email",
        notificationEnabled=True,
        isAuthority=False,
        isModerator=False,
        userID=predefined_uuids[0],
    ),
    User(
        userName="jinjie1",
        passwordHash=ph.hash("password1"),
        emailAddress="jj@example.com",
        loginStatus=False,
        points=0,
        notificationPreference="sms",
        notificationEnabled=True,
        isAuthority=False,
        isModerator=False,
        userID=predefined_uuids[1],
    ),
    User(
        userName="yunle1",
        passwordHash=ph.hash("password1"),
        emailAddress="yunle@example.com",
        loginStatus=False,
        points=0,
        notificationPreference="push",
        notificationEnabled=True,
        isAuthority=False,
        isModerator=False,
        userID=predefined_uuids[2],
    ),
    User(
        userName="weixu",
        passwordHash=ph.hash("password1"),
        emailAddress="weixu@example.com",
        loginStatus=False,
        points=0,
        notificationPreference="email",
        notificationEnabled=True,
        isAuthority=False,
        isModerator=False,
        userID=predefined_uuids[3],
    ),
    User(
        userName="amogh1",
        passwordHash=ph.hash("password1"),
        emailAddress="asriman200@gmail.com", #asriman2005@gmail.com
        loginStatus=False,
        points=0,
        notificationPreference="sms",
        notificationEnabled=True,
        isAuthority=True,
        isModerator=False,
        userID=predefined_uuids[4],
    ),
    User(
        userName="maxwell1",
        passwordHash=ph.hash("password1"),
        emailAddress="maxweliau12345@outlook.com",
        loginStatus=False,
        points=0,
        notificationPreference="sms",
        notificationEnabled=True,
        isAuthority=True,
        isModerator=False,
        userID=predefined_uuids[5],
    ),
    User(
        userName="admin",
        passwordHash=ph.hash("password1"),
        emailAddress="admin@example.com",
        loginStatus=False,
        points=0,
        notificationPreference="sms",
        notificationEnabled=True,
        isAuthority=False,
        isModerator=True,
        userID=predefined_uuids[6],
    ),
    User(
        userName="Bukit Batok Fire Station",
        passwordHash=ph.hash("password1"),  # Example password
        emailAddress="bukitbatokfirestation@example.com",  # Generates a unique email per authority
        loginStatus=False,
        points=0,
        notificationPreference="sms",
        notificationEnabled=True,
        isAuthority=True,
        isModerator=False,
        userID=predefined_uuids[7],
    ),
    User(
        userName="Tampines Police Division",
        passwordHash=ph.hash("password1"),  # Example password
        emailAddress="tampinespolicedivision@example.com",  # Generates a unique email per authority
        loginStatus=False,
        points=0,
        notificationPreference="sms",
        notificationEnabled=True,
        isAuthority=True,
        isModerator=False,
        userID=predefined_uuids[8],
    ),
    User(
        userName="Ang Mo Kio Community Center",
        passwordHash=ph.hash("password1"),  # Example password
        emailAddress="angmokiocommunitycenter@example.com",  # Generates a unique email per authority
        loginStatus=False,
        points=0,
        notificationPreference="sms",
        notificationEnabled=True,
        isAuthority=True,
        isModerator=False,
        userID=predefined_uuids[9],
    ),
    User(
        userName="Marina Bay Fire Station",
        passwordHash=ph.hash("password1"),  # Example password
        emailAddress="marinabayfirestation@example.com",  # Generates a unique email per authority
        loginStatus=False,
        points=0,
        notificationPreference="sms",
        notificationEnabled=True,
        isAuthority=True,
        isModerator=False,
        userID=predefined_uuids[10],
    ),
    User(
        userName="Woodlands Police Division",
        passwordHash=ph.hash("password1"),  # Example password
        emailAddress="woodlandspolicedivision@example.com",  # Generates a unique email per authority
        loginStatus=False,
        points=0,
        notificationPreference="sms",
        notificationEnabled=True,
        isAuthority=True,
        isModerator=False,
        userID=predefined_uuids[11],
    ),
    User(
        userName="Bedok Community Center",
        passwordHash=ph.hash("password1"),  # Example password
        emailAddress="bedokcommunitycenter@example.com",  # Generates a unique email per authority
        loginStatus=False,
        points=0,
        notificationPreference="sms",
        notificationEnabled=True,
        isAuthority=True,
        isModerator=False,
        userID=predefined_uuids[12],
    ),
    User(
        userName="Jurong Fire Station",
        passwordHash=ph.hash("password1"),  # Example password
        emailAddress="jurongfirestation@example.com",  # Generates a unique email per authority
        loginStatus=False,
        points=0,
        notificationPreference="sms",
        notificationEnabled=True,
        isAuthority=True,
        isModerator=False,
        userID=predefined_uuids[13],
    ),
    User(
        userName="Choa Chu Kang Police Post",
        passwordHash=ph.hash("password1"),  # Example password
        emailAddress="choachukangpolicepost@example.com",  # Generates a unique email per authority
        loginStatus=False,
        points=0,
        notificationPreference="sms",
        notificationEnabled=True,
        isAuthority=True,
        isModerator=False,
        userID=predefined_uuids[14],
    ),
    User(
        userName="Pasir Ris Community Center",
        passwordHash=ph.hash("password1"),  # Example password
        emailAddress="pasirriscommunitycenter@example.com",  # Generates a unique email per authority
        loginStatus=False,
        points=0,
        notificationPreference="sms",
        notificationEnabled=True,
        isAuthority=True,
        isModerator=False,
        userID=predefined_uuids[15],
    ),
    User(
        userName="Clementi Fire Station",
        passwordHash=ph.hash("password1"),  # Example password
        emailAddress="clementifirestation@example.com",  # Generates a unique email per authority
        loginStatus=False,
        points=0,
        notificationPreference="sms",
        notificationEnabled=True,
        isAuthority=True,
        isModerator=False,
        userID=predefined_uuids[16],
    ),
    User(
        userName="Hougang Neighbourhood Police",
        passwordHash=ph.hash("password1"),  # Example password
        emailAddress="hougangneighbourhoodpolice@example.com",  # Generates a unique email per authority
        loginStatus=False,
        points=0,
        notificationPreference="sms",
        notificationEnabled=True,
        isAuthority=True,
        isModerator=False,
        userID=predefined_uuids[17],
    ),
    User(
        userName="Yishun Community Center",
        passwordHash=ph.hash("password1"),  # Example password
        emailAddress="yishuncommunitycenter@example.com",  # Generates a unique email per authority
        loginStatus=False,
        points=0,
        notificationPreference="sms",
        notificationEnabled=True,
        isAuthority=True,
        isModerator=False,
        userID=predefined_uuids[18],
    ),
    User(
        userName="Geylang Fire Station",
        passwordHash=ph.hash("password1"),  # Example password
        emailAddress="geylangfirestation@example.com",  # Generates a unique email per authority
        loginStatus=False,
        points=0,
        notificationPreference="sms",
        notificationEnabled=True,
        isAuthority=True,
        isModerator=False,
        userID=predefined_uuids[19],
    ),
    User(
        userName="Kreta Ayer Police Post",
        passwordHash=ph.hash("password1"),  # Example password
        emailAddress="kretaayerpolicepost@example.com",  # Generates a unique email per authority
        loginStatus=False,
        points=0,
        notificationPreference="sms",
        notificationEnabled=True,
        isAuthority=True,
        isModerator=False,
        userID=predefined_uuids[20],
    ),
    User(
        userName="Bukit Merah Community Center",
        passwordHash=ph.hash("password1"),  # Example password
        emailAddress="bukitmerahcommunitycenter@example.com",  # Generates a unique email per authority
        loginStatus=False,
        points=0,
        notificationPreference="sms",
        notificationEnabled=True,
        isAuthority=True,
        isModerator=False,
        userID=predefined_uuids[21],
    ),
    User(
        userName="Serangoon Fire Station",
        passwordHash=ph.hash("password1"),  # Example password
        emailAddress="serangoonfirestation@example.com",  # Generates a unique email per authority
        loginStatus=False,
        points=0,
        notificationPreference="sms",
        notificationEnabled=True,
        isAuthority=True,
        isModerator=False,
        userID=predefined_uuids[22],
    ),
    User(
        userName="Sengkang Neighbourhood Police",
        passwordHash=ph.hash("password1"),  # Example password
        emailAddress="sengkangneighbourhoodpolice@example.com",  # Generates a unique email per authority
        loginStatus=False,
        points=0,
        notificationPreference="sms",
        notificationEnabled=True,
        isAuthority=True,
        isModerator=False,
        userID=predefined_uuids[23],
    ),
    User(
        userName="Bukit Panjang Community Center",
        passwordHash=ph.hash("password1"),  # Example password
        emailAddress="bukitpanjangcommunitycenter@example.com",  # Generates a unique email per authority
        loginStatus=False,
        points=0,
        notificationPreference="sms",
        notificationEnabled=True,
        isAuthority=True,
        isModerator=False,
        userID=predefined_uuids[24],
    ),
    User(
        userName="Paya Lebar Fire Post",
        passwordHash=ph.hash("password1"),  # Example password
        emailAddress="payalebarfirepost@example.com",  # Generates a unique email per authority
        loginStatus=False,
        points=0,
        notificationPreference="sms",
        notificationEnabled=True,
        isAuthority=True,
        isModerator=False,
        userID=predefined_uuids[25],
    ),
    User(
        userName="Queenstown Neighbourhood Police",
        passwordHash=ph.hash("password1"),  # Example password
        emailAddress="queenstownneighbourhoodpolice@example.com",  # Generates a unique email per authority
        loginStatus=False,
        points=0,
        notificationPreference="sms",
        notificationEnabled=True,
        isAuthority=True,
        isModerator=False,
        userID=predefined_uuids[26],
    ),
    User(
        userName="Toa Payoh Central Community Center",
        passwordHash=ph.hash("password1"),  # Example password
        emailAddress="toapayohcentralcommunitycenter@example.com",  # Generates a unique email per authority
        loginStatus=False,
        points=0,
        notificationPreference="sms",
        notificationEnabled=True,
        isAuthority=True,
        isModerator=False,
        userID=predefined_uuids[27],
    ),
    User(
        userName="Tan Tock Seng Hospital",
        passwordHash=ph.hash("password1"),  # Example password
        emailAddress="tantocksenghospital@example.com",  # Generates a unique email per authority
        loginStatus=False,
        points=0,
        notificationPreference="sms",
        notificationEnabled=True,
        isAuthority=True,
        isModerator=False,
        userID=predefined_uuids[28],
    ),
    User(
        userName="Singapore General Hospital",
        passwordHash=ph.hash("password1"),  # Example password
        emailAddress="singaporegeneralhospital@example.com",  # Generates a unique email per authority
        loginStatus=False,
        points=0,
        notificationPreference="sms",
        notificationEnabled=True,
        isAuthority=True,
        isModerator=False,
        userID=predefined_uuids[29],
    ),
    User(
        userName="Khoo Teck Puat Hospital",
        passwordHash=ph.hash("password1"),  # Example password
        emailAddress="khooteckpuathospital@example.com",  # Generates a unique email per authority
        loginStatus=False,
        points=0,
        notificationPreference="sms",
        notificationEnabled=True,
        isAuthority=True,
        isModerator=False,
        userID=predefined_uuids[30],
    ),
    User(
        userName="Changi General Hospital",
        passwordHash=ph.hash("password1"),  # Example password
        emailAddress="changigeneralhospital@example.com",  # Generates a unique email per authority
        loginStatus=False,
        points=0,
        notificationPreference="sms",
        notificationEnabled=True,
        isAuthority=True,
        isModerator=False,
        userID=predefined_uuids[31],
    ),
    User(
        userName="Mount Elizabeth Hospital",
        passwordHash=ph.hash("password1"),  # Example password
        emailAddress="mountelizabethhospital@example.com",  # Generates a unique email per authority
        loginStatus=False,
        points=0,
        notificationPreference="sms",
        notificationEnabled=True,
        isAuthority=True,
        isModerator=False,
        userID=predefined_uuids[32],
    ),
    User(
        userName="KK Women's and Children's Hospital",
        passwordHash=ph.hash("password1"),  # Example password
        emailAddress="kkwomen'sandchildren'shospital@example.com",  # Generates a unique email per authority
        loginStatus=False,
        points=0,
        notificationPreference="sms",
        notificationEnabled=True,
        isAuthority=True,
        isModerator=False,
        userID=predefined_uuids[33],
    ),
    User(
        userName="Singapore Civil Defence Force HQ",
        passwordHash=ph.hash("password1"),  # Example password
        emailAddress="singaporecivildefenceforcehq@example.com",  # Generates a unique email per authority
        loginStatus=False,
        points=0,
        notificationPreference="sms",
        notificationEnabled=True,
        isAuthority=True,
        isModerator=False,
        userID=predefined_uuids[34],
    ),
    User(
        userName="Police Cantonment Complex",
        passwordHash=ph.hash("password1"),  # Example password
        emailAddress="policecantonmentcomplex@example.com",  # Generates a unique email per authority
        loginStatus=False,
        points=0,
        notificationPreference="sms",
        notificationEnabled=True,
        isAuthority=True,
        isModerator=False,
        userID=predefined_uuids[35],
    ),
    User(
        userName="Clementi Neighbourhood Police Centre",
        passwordHash=ph.hash("password1"),  # Example password
        emailAddress="clementineighbourhoodpolicecentre@example.com",  # Generates a unique email per authority
        loginStatus=False,
        points=0,
        notificationPreference="sms",
        notificationEnabled=True,
        isAuthority=True,
        isModerator=False,
        userID=predefined_uuids[36],
    ),
    User(
        userName="Eunos Fire Station",
        passwordHash=ph.hash("password1"),  # Example password
        emailAddress="eunosfirestation@example.com",  # Generates a unique email per authority
        loginStatus=False,
        points=0,
        notificationPreference="sms",
        notificationEnabled=True,
        isAuthority=True,
        isModerator=False,
        userID=predefined_uuids[37],
    ),
    User(
        userName="Bukit Timah Community Club",
        passwordHash=ph.hash("password1"),  # Example password
        emailAddress="bukittimahcommunityclub@example.com",  # Generates a unique email per authority
        loginStatus=False,
        points=0,
        notificationPreference="sms",
        notificationEnabled=True,
        isAuthority=True,
        isModerator=False,
        userID=predefined_uuids[38],
    ),
    User(
        userName="Jurong West Police Division",
        passwordHash=ph.hash("password1"),  # Example password
        emailAddress="jurongwestpolicedivision@example.com",  # Generates a unique email per authority
        loginStatus=False,
        points=0,
        notificationPreference="sms",
        notificationEnabled=True,
        isAuthority=True,
        isModerator=False,
        userID=predefined_uuids[39],
    ),
    User(
        userName="Toa Payoh Fire Station",
        passwordHash=ph.hash("password1"),  # Example password
        emailAddress="toapayohfirestation@example.com",  # Generates a unique email per authority
        loginStatus=False,
        points=0,
        notificationPreference="sms",
        notificationEnabled=True,
        isAuthority=True,
        isModerator=False,
        userID=predefined_uuids[40],
    ),
    User(
        userName="Potong Pasir Community Center",
        passwordHash=ph.hash("password1"),  # Example password
        emailAddress="potongpasircommunitycenter@example.com",  # Generates a unique email per authority
        loginStatus=False,
        points=0,
        notificationPreference="sms",
        notificationEnabled=True,
        isAuthority=True,
        isModerator=False,
        userID=predefined_uuids[41],
    ),
    User(
        userName="Ghim Moh Community Center",
        passwordHash=ph.hash("password1"),  # Example password
        emailAddress="ghimmohcommunitycenter@example.com",  # Generates a unique email per authority
        loginStatus=False,
        points=0,
        notificationPreference="sms",
        notificationEnabled=True,
        isAuthority=True,
        isModerator=False,
        userID=predefined_uuids[42],
    ),
    User(
        userName="Yew Tee Neighbourhood Police",
        passwordHash=ph.hash("password1"),  # Example password
        emailAddress="yewteeneighbourhoodpolice@example.com",  # Generates a unique email per authority
        loginStatus=False,
        points=0,
        notificationPreference="sms",
        notificationEnabled=True,
        isAuthority=True,
        isModerator=False,
        userID=predefined_uuids[43],
    ),
    User(
        userName="Kallang Fire Station",
        passwordHash=ph.hash("password1"),  # Example password
        emailAddress="kallangfirestation@example.com",  # Generates a unique email per authority
        loginStatus=False,
        points=0,
        notificationPreference="sms",
        notificationEnabled=True,
        isAuthority=True,
        isModerator=False,
        userID=predefined_uuids[44],
    ),
    User(
        userName="Tanglin Neighbourhood Police",
        passwordHash=ph.hash("password1"),  # Example password
        emailAddress="tanglinneighbourhoodpolice@example.com",  # Generates a unique email per authority
        loginStatus=False,
        points=0,
        notificationPreference="sms",
        notificationEnabled=True,
        isAuthority=True,
        isModerator=False,
        userID=predefined_uuids[45],
    ),
    User(
        userName="Sembawang Community Center",
        passwordHash=ph.hash("password1"),  # Example password
        emailAddress="sembawangcommunitycenter@example.com",  # Generates a unique email per authority
        loginStatus=False,
        points=0,
        notificationPreference="sms",
        notificationEnabled=True,
        isAuthority=True,
        isModerator=False,
        userID=predefined_uuids[46],
    ),
    User(
        userName="Nanyang Community Center",
        passwordHash=ph.hash("password1"),  # Example password
        emailAddress="nanyangcommunitycenter@example.com",  # Generates a unique email per authority
        loginStatus=False,
        points=0,
        notificationPreference="sms",
        notificationEnabled=True,
        isAuthority=True,
        isModerator=False,
        userID=predefined_uuids[47],
    ),
    User(
        userName="Orchard Neighbourhood Police",
        passwordHash=ph.hash("password1"),  # Example password
        emailAddress="orchardneighbourhoodpolice@example.com",  # Generates a unique email per authority
        loginStatus=False,
        points=0,
        notificationPreference="sms",
        notificationEnabled=True,
        isAuthority=True,
        isModerator=False,
        userID=predefined_uuids[48],
    ),
    User(
        userName="Cairnhill Community Center",
        passwordHash=ph.hash("password1"),  # Example password
        emailAddress="cairnhillcommunitycenter@example.com",  # Generates a unique email per authority
        loginStatus=False,
        points=0,
        notificationPreference="sms",
        notificationEnabled=True,
        isAuthority=True,
        isModerator=False,
        userID=predefined_uuids[49],
    ),
    User(
        userName="Sentosa Fire Station",
        passwordHash=ph.hash("password1"),  # Example password
        emailAddress="sentosafirestation@example.com",  # Generates a unique email per authority
        loginStatus=False,
        points=0,
        notificationPreference="sms",
        notificationEnabled=True,
        isAuthority=True,
        isModerator=False,
        userID=predefined_uuids[50],
    ),
    User(
        userName="Outram Community Center",
        passwordHash=ph.hash("password1"),  # Example password
        emailAddress="outramcommunitycenter@example.com",  # Generates a unique email per authority
        loginStatus=False,
        points=0,
        notificationPreference="sms",
        notificationEnabled=True,
        isAuthority=True,
        isModerator=False,
        userID=predefined_uuids[51],
    ),
    User(
        userName="Harbourfront Fire Post",
        passwordHash=ph.hash("password1"),  # Example password
        emailAddress="harbourfrontfirepost@example.com",  # Generates a unique email per authority
        loginStatus=False,
        points=0,
        notificationPreference="sms",
        notificationEnabled=True,
        isAuthority=True,
        isModerator=False,
        userID=predefined_uuids[52],
    ),
    User(
        userName="Chinatown Neighbourhood Police",
        passwordHash=ph.hash("password1"),  # Example password
        emailAddress="chinatownneighbourhoodpolice@example.com",  # Generates a unique email per authority
        loginStatus=False,
        points=0,
        notificationPreference="sms",
        notificationEnabled=True,
        isAuthority=True,
        isModerator=False,
        userID=predefined_uuids[53],
    ),
    User(
        userName="Marine Parade Community Center",
        passwordHash=ph.hash("password1"),  # Example password
        emailAddress="marineparadecommunitycenter@example.com",  # Generates a unique email per authority
        loginStatus=False,
        points=0,
        notificationPreference="sms",
        notificationEnabled=True,
        isAuthority=True,
        isModerator=False,
        userID=predefined_uuids[54],
    ),
    User(
        userName="Newton Police Division",
        passwordHash=ph.hash("password1"),  # Example password
        emailAddress="newtonpolicedivision@example.com",  # Generates a unique email per authority
        loginStatus=False,
        points=0,
        notificationPreference="sms",
        notificationEnabled=True,
        isAuthority=True,
        isModerator=False,
        userID=predefined_uuids[55],
    ),
    User(
        userName="Kovan Fire Station",
        passwordHash=ph.hash("password1"),  # Example password
        emailAddress="kovanfirestation@example.com",  # Generates a unique email per authority
        loginStatus=False,
        points=0,
        notificationPreference="sms",
        notificationEnabled=True,
        isAuthority=True,
        isModerator=False,
        userID=predefined_uuids[56],
    ),
    User(
        userName="MacPherson Neighbourhood Police",
        passwordHash=ph.hash("password1"),  # Example password
        emailAddress="macphersonneighbourhoodpolice@example.com",  # Generates a unique email per authority
        loginStatus=False,
        points=0,
        notificationPreference="sms",
        notificationEnabled=True,
        isAuthority=True,
        isModerator=False,
        userID=predefined_uuids[57],
    ),
]

# Insert each dummy user into the database
for user in dummy_users:
    create_user(user)

conn.close()
