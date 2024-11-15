# Reports API Documentation

The `reports` API allows users to create, retrieve, update, and delete reports, along with searching and filtering options. The API also supports uploading images associated with reports and retrieving them based on report ID.

## Table of Contents

-   [Setup](#setup)
-   [API Endpoints](#api-endpoints)
    -   [Create Report](#create-report)
    -   [Get Reports by User ID](#get-reports-by-user-id)
    -   [Get Top K Reports by Severity](#get-top-k-reports-by-severity)
    -   [Read Report by ID](#read-report-by-id)
    -   [Get Reports by Authority ID](#get-reports-by-authority-id)
    -   [Search Reports by Description](#search-reports-by-description)
    -   [Search Reports by Title](#search-reports-by-title)
    -   [Submit Report with Image](#submit-report-with-image)
    -   [Delete Report](#delete-report)
    -   [Update Report Status](#update-report-status)
    -   [Get Report Picture](#get-report-picture)

---

## Setup

1. **Requirements**:
    - Install dependencies: `fastapi`, `sqlite3`, `Pillow`, and `asyncio`.
2. **Directory Structure**:
    - Place images in the `img/reportimg/` directory.

## API Endpoints

### Create Report

`POST /reports/`

Creates a new report.

-   **Request Body**: `Report` model instance.
-   **Response**: Created `Report` object.
-   **Status Codes**:
    -   `201`: Report created successfully.
    -   `400`: Bad request.
    -   `500`: Internal server error.

### Get Reports by User ID

`GET /reports/user/{user_id}`

Retrieves all reports submitted by a specific user.

-   **Path Parameters**:
    -   `user_id` (str): ID of the user.
-   **Response**: List of `Report` objects.
-   **Status Codes**:
    -   `200`: Success.
    -   `500`: Failed to retrieve reports.

### Get Top K Reports by Severity

`GET /reports/top/{k}/{resolved}`

Retrieves the top `k` reports based on severity.

-   **Path Parameters**:
    -   `k` (int): Number of reports to retrieve.
    -   `resolved` (bool): Filter resolved reports.
-   **Response**: List of top `k` `Report` objects.
-   **Status Codes**:
    -   `200`: Success.
    -   `500`: Failed to retrieve reports.

### Read Report by ID

`GET /reports/{report_id}`

Retrieves a report by its ID.

-   **Path Parameters**:
    -   `report_id` (str): ID of the report.
-   **Response**: `Report` object if found.
-   **Status Codes**:
    -   `200`: Success.
    -   `404`: Report not found.
    -   `500`: Failed to retrieve report.

### Get Reports by Authority ID

`GET /reports/get_reports_by_authority_id/{authority_id}`

Retrieves all reports associated with a specific authority.

-   **Path Parameters**:
    -   `authority_id` (str): ID of the authority.
-   **Response**: List of `Report` objects.
-   **Status Codes**:
    -   `200`: Success.
    -   `500`: Failed to retrieve reports.

### Search Reports by Description

`GET /reports/search/description`

Searches for reports based on description.

-   **Query Parameters**:
    -   `description` (str): Description text to search for.
-   **Response**: List of `Report` objects.
-   **Status Codes**:
    -   `200`: Success.
    -   `500`: Failed to search reports.

### Search Reports by Title

`GET /reports/search/title`

Searches for reports based on title.

-   **Query Parameters**:
    -   `title` (str): Title text to search for.
-   **Response**: List of `Report` objects.
-   **Status Codes**:
    -   `200`: Success.
    -   `500`: Failed to search reports.

### Submit Report with Image

`POST /reports/submit-report/`

Submits a report with an image upload.

-   **Form Parameters**:
    -   `user_id` (str): ID of the user.
    -   `description` (str, optional): Description of the report.
    -   `title` (str, optional): Title of the report.
    -   `longitude` (float, optional): Longitude of the location.
    -   `latitude` (float, optional): Latitude of the location.
    -   `incident_time` (int, optional): Timestamp of the incident.
    -   `image` (UploadFile): Image file of the report.
-   **Response**: JSON message confirming receipt.
-   **Status Codes**:
    -   `200`: Report received.
    -   `400`: Missing or invalid data.
    -   `404`: User not found.
    -   `500`: Failed to save image.

### Delete Report

`DELETE /reports/{report_id}`

Deletes a report by its ID.

-   **Path Parameters**:
    -   `report_id` (str): ID of the report.
-   **Response**: JSON message confirming deletion.
-   **Status Codes**:
    -   `200`: Report deleted successfully.
    -   `404`: Report not found.
    -   `500`: Failed to delete report.

### Update Report Status

`PUT /reports/{report_id}/status`

Updates the status of a report.

-   **Path Parameters**:
    -   `report_id` (str): ID of the report.
-   **Body**: JSON object with `status` field.
-   **Response**: JSON message confirming update.
-   **Status Codes**:
    -   `200`: Status updated.
    -   `404`: Report not found.
    -   `500`: Failed to update status.

### Get Report Picture

`GET /reports/reportPicture/{report_id}`

Retrieves the image associated with a report by its ID.

-   **Path Parameters**:
    -   `report_id` (uuid.UUID): ID of the report.
-   **Response**: Image file if found, else a default image.
-   **Status Codes**:
    -   `200`: Image returned.
    -   `404`: Report image not found, default returned.

---
