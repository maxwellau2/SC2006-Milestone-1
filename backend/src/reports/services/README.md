# Documentation for Service

-   [OllamaChat Documentation](#OllamaChat)
-   [PointsService Documentation](#PointsService)
-   [ReportService Documentation](#ReportService)
-   [telegramBot Documentation](#telegramBot)

---

# OllamaChat

The `OllamaChat` class provides functionality for text and image analysis using the Ollama model. It can handle tasks such as generating text responses, analyzing images, comparing image descriptions to textual descriptions, and identifying the nearest relevant authority.

## Table of Contents

-   [Overview](#overview)
-   [Setup Instructions](#setup-instructions)
-   [Methods](#methods)
    -   [ask](#ask)
    -   [analyze_image](#analyze_image)
    -   [compare_analysis_and_description](#compare_analysis_and_description)
    -   [analyse_image_and_text](#analyse_image_and_text)
    -   [find_nearest_authority](#find_nearest_authority)
    -   [haversine](#haversine)
    -   [get_relevant_authority_ollama](#get_relevant_authority_ollama)

## Overview

`OllamaChat` allows for text and image-based inquiries using the Ollama model, with methods for generating responses, analyzing images, and assessing relevance, severity, and urgency based on given descriptions. It can locate the closest authority based on input coordinates and classify relevant authorities based on descriptions.

## Setup Instructions

1. Ensure `ollama`, `aiofiles`, `numpy`, and `pandas` libraries are installed.
2. Place `authorities.csv` in the `database/` directory, containing details on various authorities and their coordinates.

## Methods

### ask

```python
async def ask(self, prompt: str) -> str
```

Generates a text response based on a prompt using the specified model.

-   **Parameters**:
    -   `prompt` (str): The text prompt for analysis.
-   **Returns**: `str` – The generated response.

### analyze_image

```python
async def analyze_image(self, image_path: str, prompt: str) -> str
```

Analyzes an image asynchronously based on a given prompt using the `llava` model.

-   **Parameters**:
    -   `image_path` (str): Path to the image file.
    -   `prompt` (str): Prompt for analyzing the image.
-   **Returns**: `str` – The analysis result.

### compare_analysis_and_description

```python
async def compare_analysis_and_description(self, image_analysis: str, text_description: str) -> str
```

Compares the results of an image analysis with a textual description and provides ratings for relevance, severity, and urgency.

-   **Parameters**:
    -   `image_analysis` (str): Analysis of the image.
    -   `text_description` (str): Description to compare with the image.
-   **Returns**: `str` – Ratings in the format "X,Y,Z" (Relevance, Severity, Urgency).

### analyse_image_and_text

```python
async def analyse_image_and_text(self, image_path: str, image_prompt: str, text_description: str) -> dict
```

Performs a combined analysis of an image and text description, returning ratings, a generated title, and image analysis.

-   **Parameters**:
    -   `image_path` (str): Path to the image file.
    -   `image_prompt` (str): Prompt for analyzing the image.
    -   `text_description` (str): Description to use for comparison.
-   **Returns**: `dict` – Contains `ratings`, `title`, and `analysis`.

### find_nearest_authority

```python
async def find_nearest_authority(self, input_lat: float, input_lon: float, authority_type: str) -> dict
```

Finds the nearest authority of a specified type based on latitude and longitude, using the Haversine formula for distance calculation.

-   **Parameters**:
    -   `input_lat` (float): Latitude of the input location.
    -   `input_lon` (float): Longitude of the input location.
    -   `authority_type` (str): Type of authority to locate (e.g., "Police Station").
-   **Returns**: `dict` – Information on the nearest authority, including name, coordinates, and distance.

### haversine

```python
def haversine(self, lat1, lon1, lat2, lon2) -> float
```

Calculates the distance between two geographic points using the Haversine formula.

-   **Parameters**:
    -   `lat1` (float): Latitude of the first point.
    -   `lon1` (float): Longitude of the first point.
    -   `lat2` (float): Latitude of the second point.
    -   `lon2` (float): Longitude of the second point.
-   **Returns**: `float` – Distance in kilometers between the two points.

### get_relevant_authority_ollama

```python
async def get_relevant_authority_ollama(self, description: str) -> str
```

Determines the most relevant authority type based on a textual description by comparing it to a list of possible authorities.

-   **Parameters**:
    -   `description` (str): Text description to classify.
-   **Returns**: `str` – The identified relevant authority type or "Unknown" if no match is found.

---

# PointsService

The `PointsService` class manages user points, evaluates reports, and interacts with external services like Ollama and Telegram. It provides methods for creating users, updating points based on report ratings, and notifying relevant authorities.

## Table of Contents

-   [Overview](#overview)
-   [Database Schema](#database-schema)
-   [Setup Instructions](#setup-instructions)
-   [Methods](#methods)
    -   [create_user](#create_user)
    -   [check_user_exists](#check_user_exists)
    -   [get_point_from_user_id](#get_point_from_user_id)
    -   [update_point_for_user_id](#update_point_for_user_id)
    -   [update_ratings](#update_ratings)
    -   [calculate_points](#calculate_points)
    -   [evaluate_points](#evaluate_points)
    -   [evaluate_and_add_points](#evaluate_and_add_points)
    -   [set_ollama_description](#set_ollama_description)
    -   [set_authority_id](#set_authority_id)
    -   [set_report_status_in_progress](#set_report_status_in_progress)
    -   [update_title](#update_title)
    -   [wipe_clean](#wipe_clean)

## Overview

`PointsService` is responsible for managing user points, evaluating reports with the help of the `OllamaChat` service, updating the `User` table, and notifying authorities using `telegramBot`.

## Database Schema

### User Table

-   **userID** (TEXT): Unique identifier for the user.
-   **userName** (TEXT): Default username for the user.
-   **points** (INTEGER): User's points accumulated from report evaluations.
-   Additional columns are assumed based on user attributes, such as `emailAddress`, `notificationPreference`, and more.

### Report Table

-   **ReportID** (TEXT, Primary Key): Unique identifier for each report.
-   **relevance**, **severity**, **urgency** (INTEGER): Ratings for report.
-   **points** (INTEGER): Points associated with the report.
-   **title** (TEXT): Title of the report.
-   **Status** (TEXT): Status of the report (`Pending`, `In Progress`, etc.).
-   **AuthorityID** (TEXT): Identifier for the assigned authority.
-   **OllamaDescription** (TEXT): Description generated by Ollama.

## Setup Instructions

1. Ensure SQLite3 and `database/users.db` and `database/reports.db` are available in the project directory.
2. Requires `OllamaChat` and `telegramBot` classes and a Telegram Bot API token.

## Methods

### create_user

```python
def create_user(self, user_id: str) -> None
```

Creates a new user with initial points set to 0 if the user does not already exist.

-   **Parameters**:
    -   `user_id` (str): Unique identifier for the user.
-   **Returns**: None.

### check_user_exists

```python
def check_user_exists(self, user_id: str) -> bool
```

Checks if a user exists in the `User` table. If not, creates the user.

-   **Parameters**:
    -   `user_id` (str): Unique identifier for the user.
-   **Returns**: `bool` – True if user exists, False otherwise.

### get_point_from_user_id

```python
def get_point_from_user_id(self, user_id: str) -> int
```

Retrieves the points for a specific user.

-   **Parameters**:
    -   `user_id` (str): Unique identifier for the user.
-   **Returns**: `int` – Points of the user, or 0 if user not found.

### update_point_for_user_id

```python
def update_point_for_user_id(self, user_id: str, points: int, report_id: str) -> int
```

Updates points for a user in the `User` table and logs points in the associated report.

-   **Parameters**:
    -   `user_id` (str): Unique identifier for the user.
    -   `points` (int): New points to assign to the user.
    -   `report_id` (str): Identifier of the associated report.
-   **Returns**: `int` – Status code (`200` for success, `404` if user not found).

### update_ratings

```python
def update_ratings(self, report_id: str, ratings: tuple[int], points: int) -> int
```

Updates relevance, severity, urgency, and points for a report in the `Report` table.

-   **Parameters**:
    -   `report_id` (str): Unique identifier for the report.
    -   `ratings` (tuple[int]): Ratings (relevance, severity, urgency).
    -   `points` (int): Points to assign to the report.
-   **Returns**: `int` – Status code (`200` for success, `404` if report not found).

### calculate_points

```python
@staticmethod
def calculate_points(ratings: list[int]) -> int
```

Calculates points based on relevance, severity, and urgency ratings.

-   **Parameters**:
    -   `ratings` (list[int]): Ratings (relevance, severity, urgency).
-   **Returns**: `int` – Calculated points.

### evaluate_points

```python
async def evaluate_points(self, image_path: str, text_description: str) -> tuple[int, tuple[int]]
```

Evaluates points based on image and description analysis, providing ratings and points.

-   **Parameters**:
    -   `image_path` (str): Path to the image for analysis.
    -   `text_description` (str): Description for comparison.
-   **Returns**: `tuple` – `(points, (relevance, severity, urgency), title, analysis)`.

### evaluate_and_add_points

```python
async def evaluate_and_add_points(self, report: Report) -> None
```

Evaluates points for a report, updates the user’s points, and assigns relevant authority.

-   **Parameters**:
    -   `report` (Report): The report to evaluate and log points for.
-   **Returns**: None.

### set_ollama_description

```python
def set_ollama_description(self, report_id: str, description: str) -> int
```

Sets the Ollama-generated description for a report in the `Report` table.

-   **Parameters**:
    -   `report_id` (str): Unique identifier for the report.
    -   `description` (str): Description text to store.
-   **Returns**: `int` – Status code (`200` for success, `404` if report not found).

### set_authority_id

```python
def set_authority_id(self, report_id: str, authority_id: str) -> int
```

Sets the authority ID for a report in the `Report` table.

-   **Parameters**:
    -   `report_id` (str): Unique identifier for the report.
    -   `authority_id` (str): Identifier of the authority to assign.
-   **Returns**: `int` – Status code (`200` for success, `404` if report not found).

### set_report_status_in_progress

```python
def set_report_status_in_progress(self, report_id: str) -> int
```

Updates the status of a report to "In Progress" in the `Report` table.

-   **Parameters**:
    -   `report_id` (str): Unique identifier for the report.
-   **Returns**: `int` – Status code (`200` for success, `404` if report not found).

### update_title

```python
def update_title(self, report_id: str, title: str) -> int
```

Updates the title for a report in the `Report` table if the title field is empty.

-   **Parameters**:
    -   `report_id` (str): Unique identifier for the report.
    -   `title` (str): Title to set for the report.
-   **Returns**: `int` – Status code (`200` for success, `404` if report not found).

### wipe_clean

```python
async def wipe_clean(self) -> int
```

Clears all points from the `User` table, retaining other user information.

-   **Returns**: `int` – Status code (`200` for success, `500` for internal error).

---

# ReportService

The `ReportService` class manages CRUD operations and queries on reports within the `Report` table in an SQLite database. It provides methods for creating, reading, updating, and deleting reports, as well as various search and filtering functionalities.

## Table of Contents

-   [Overview](#overview)
-   [Database Schema](#database-schema)
-   [Setup Instructions](#setup-instructions)
-   [Methods](#methods)
    -   [create_report_table](#create_report_table)
    -   [create_report](#create_report)
    -   [check_report_exists](#check_report_exists)
    -   [read_report_by_authority_id](#read_report_by_authority_id)
    -   [update_report_status](#update_report_status)
    -   [read_report_by_user_id](#read_report_by_user_id)
    -   [get_top_k_reports_by_severity](#get_top_k_reports_by_severity)
    -   [read_report_by_id](#read_report_by_id)
    -   [search_reports_by_description](#search_reports_by_description)
    -   [search_reports_by_title](#search_reports_by_title)
    -   [delete_report_by_id](#delete_report_by_id)
    -   [update_report_points](#update_report_points)
    -   [\_parse_report](#_parse_report)
    -   [close_connection](#close_connection)
    -   [check_user_exists](#check_user_exists)

## Overview

The `ReportService` class provides comprehensive database operations for the `Report` table. It supports the creation of reports, updating statuses and points, and retrieving reports based on different criteria such as user ID, authority ID, and severity.

## Database Schema

The `Report` table schema includes the following columns:

-   **UserID** (TEXT, Not Null): User who created the report.
-   **Relevance**, **Severity**, **Urgency** (INTEGER): Ratings for the report.
-   **Status** (TEXT): Status of the report, constrained to values: `'Pending'`, `'In Progress'`, or `'Resolved'`.
-   **ReportID** (TEXT, Primary Key): Unique identifier for each report.
-   **Description** (TEXT): Description of the report.
-   **imagePath** (TEXT): Path to an associated image.
-   **Title** (TEXT): Title of the report.
-   **Datetime** (INTEGER, Not Null): Timestamp of report creation.
-   **Location** (TEXT, Not Null): Location where the report was made.
-   **Points** (INTEGER): Points assigned to the report.
-   **OllamaDescription** (TEXT): Additional description generated by the system.

## Setup Instructions

1. Ensure `sqlite3` is installed on your system.
2. Set up the `Report` table using the `create_report_table` method if it doesn't already exist.
3. Import the `ReportService` class and initialize it with a valid database connection.

## Methods

### create_report_table

```python
def create_report_table(self)
```

Creates the `Report` table in the database if it doesn't exist.

-   **Returns**: None

### create_report

```python
def create_report(self, report: Report) -> Tuple[int, Optional[Report]]
```

Inserts a new report into the `Report` table.

-   **Parameters**:
    -   `report` (Report): An instance of `Report` containing the data to insert.
-   **Returns**: `(201, Report)` if created successfully, `(400, None)` if duplicate `report_id`, `(500, None)` if internal error.

### check_report_exists

```python
def check_report_exists(self, report_id: str) -> bool
```

Checks if a report exists in the database by `ReportID`.

-   **Parameters**:
    -   `report_id` (str): Unique identifier for the report.
-   **Returns**: `bool` – True if report exists, False otherwise.

### read_report_by_authority_id

```python
def read_report_by_authority_id(self, authority_id: str) -> Tuple[int, List[Report]]
```

Retrieves all reports associated with a specific authority ID.

-   **Parameters**:
    -   `authority_id` (str): ID of the authority to filter reports by.
-   **Returns**: `(200, List[Report])` if successful, or `(500, [])` if an error occurred.

### update_report_status

```python
def update_report_status(self, report_id: str, status: str) -> int
```

Updates the status of a report.

-   **Parameters**:
    -   `report_id` (str): Unique identifier for the report.
    -   `status` (str): New status value.
-   **Returns**: `200` if successful, `404` if report not found.

### read_report_by_user_id

```python
def read_report_by_user_id(self, user_id: str) -> Tuple[int, List[Report]]
```

Retrieves all reports created by a specific user.

-   **Parameters**:
    -   `user_id` (str): Unique identifier for the user.
-   **Returns**: `(200, List[Report])` if successful, or `(500, [])` if an error occurred.

### get_top_k_reports_by_severity

```python
def get_top_k_reports_by_severity(self, k: int, resolved: bool = False) -> Tuple[int, List[Report]]
```

Fetches the top `k` reports based on severity, optionally filtering for unresolved reports.

-   **Parameters**:
    -   `k` (int): Number of reports to retrieve.
    -   `resolved` (bool): Set to True to include resolved reports, False for unresolved only.
-   **Returns**: `(200, List[Report])` if successful, or `(500, [])` if an error occurred.

### read_report_by_id

```python
def read_report_by_id(self, report_id: str) -> Tuple[int, Optional[Report]]
```

Retrieves a report by its unique `ReportID`.

-   **Parameters**:
    -   `report_id` (str): Unique identifier for the report.
-   **Returns**: `(200, Report)` if found, `(404, None)` if not found.

### search_reports_by_description

```python
def search_reports_by_description(self, description: str) -> Tuple[int, List[Report]]
```

Searches reports by description using a wildcard pattern.

-   **Parameters**:
    -   `description` (str): Description keyword to search for.
-   **Returns**: `(200, List[Report])` if successful, or `(500, [])` if an error occurred.

### search_reports_by_title

```python
def search_reports_by_title(self, title: str) -> Tuple[int, List[Report]]
```

Searches reports by title using a wildcard pattern.

-   **Parameters**:
    -   `title` (str): Title keyword to search for.
-   **Returns**: `(200, List[Report])` if successful, or `(500, [])` if an error occurred.

### delete_report_by_id

```python
def delete_report_by_id(self, report_id: str) -> int
```

Deletes a report by its unique `ReportID`.

-   **Parameters**:
    -   `report_id` (str): Unique identifier for the report.
-   **Returns**: `200` if deletion successful, `404` if report not found.

### update_report_points

```python
def update_report_points(self, report_id: str, points: int) -> int
```

Updates the points of a specific report.

-   **Parameters**:
    -   `report_id` (str): Unique identifier for the report.
    -   `points` (int): Points to assign to the report.
-   **Returns**: `200` if successful, or `500` if an error occurred.

### \_parse_report

```python
def _parse_report(self, result: Tuple) -> dict
```

Helper method to parse a row from the `Report` table into a `Report` dictionary.

-   **Parameters**:
    -   `result` (Tuple): Row data from the `Report` table.
-   **Returns**: `dict` – Parsed report data as a dictionary.

### close_connection

```python
def close_connection(self)
```

Closes the database connection.

-   **Returns**: None

### check_user_exists

```python
def check_user_exists(self, user_id: str) -> bool
```

Checks if a user exists in the `User` table, using `UserService`.

-   **Parameters**:
    -   `user_id` (str): Unique identifier for the user.
-   **Returns**: `bool` – True if user exists, False otherwise.

---

# telegramBot

The `telegramBot` class provides functionality to interact with Telegram’s Bot API, allowing sending messages, downloading images, and polling responses. It enables communication with a specific chat ID or multiple users, and handles Telegram Bot API requests.

## Table of Contents

-   [Overview](#overview)
-   [Setup Instructions](#setup-instructions)
-   [Methods](#methods)
    -   [sendText](#sendText)
    -   [sendTextToChatID](#sendTextToChatID)
    -   [downloadImage](#downloadImage)
    -   [pollResponse](#pollResponse)

## Overview

The `telegramBot` class allows for sending text messages, downloading images, and receiving responses from users. The bot can poll for specific user responses or listen to multiple users, making it versatile for applications that require real-time feedback.

## Setup Instructions

1. Obtain a bot token from [@BotFather](https://core.telegram.org/bots#botfather) on Telegram.
2. Determine your chat ID by visiting `https://api.telegram.org/bot<YourBotToken>/getUpdates` and sending a message to the bot. Your chat ID will appear in the response.
3. Initialize the `telegramBot` instance with the bot token and chat ID.

## Methods

### sendText

```python
def sendText(self, msg: str) -> bool
```

Sends a text message to the configured chat ID.

-   **Parameters**:
    -   `msg` (str): The message to send.
-   **Returns**: `bool` – True if the message was sent successfully.

### sendTextToChatID

```python
def sendTextToChatID(self, msg: str, chatid: str) -> bool
```

Sends a text message to a specified chat ID, allowing for communication with different users.

-   **Parameters**:
    -   `msg` (str): The message to send.
    -   `chatid` (str): Target chat ID to send the message to.
-   **Returns**: `bool` – True if the message was sent successfully.

### downloadImage

```python
def downloadImage(self, url: str, filename: str) -> None
```

Downloads an image from a given URL and saves it to the specified filename.

-   **Parameters**:
    -   `url` (str): URL of the image to download.
    -   `filename` (str): Filename to save the image as.
-   **Returns**: None

### pollResponse

```python
def pollResponse(self, specificity: bool, wait_time: int)
```

Polls for a response from users, either targeting a specific chat ID or allowing all users. It retrieves either text or image responses, based on messages received.

-   **Parameters**:
    -   `specificity` (bool): Set to True to listen to only the configured chat ID, or False to listen to all users.
    -   `wait_time` (int): Duration in seconds to poll for a response.
-   **Returns**: `dict` – Contains response type (`'text'` or `'image'`), response content, and the chat ID.

---
