import pytest
import requests
from fastapi import status
from uuid import uuid4
import time

BASE_URL = "http://localhost:8000/reports/reports"
TEST_USER_ID = "123e4567-e89b-12d3-a456-426614174000"  # Example user ID
TEST_REPORT_ID = str(uuid4())

image_path = "src/reports/test_api/hotdogcat.png"


@pytest.fixture(scope="module")
def client():
    """Setup base URL for the API."""
    return BASE_URL


def test_get_reports_by_user_id(client):
    """Test retrieving reports by user ID."""
    response = requests.get(f"{client}/user/{TEST_USER_ID}")
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list), "Expected a list of reports"


def test_get_top_k_reports_by_severity(client):
    """Test retrieving top k reports by severity."""
    response = requests.get(f"{client}/top/5/false")
    assert response.status_code == status.HTTP_200_OK
    reports = response.json()
    assert isinstance(reports, list), "Expected a list of reports"
    assert len(reports) <= 5, "More than expected number of reports"


def test_read_report_by_id(client):
    """Test retrieving a report by ID."""
    response = requests.get(f"{client}/{TEST_REPORT_ID}")
    if response.status_code == status.HTTP_200_OK:
        report = response.json()
        assert report["report_id"] == TEST_REPORT_ID
    elif response.status_code == status.HTTP_404_NOT_FOUND:
        assert response.json()["detail"] == "Report not found"


def test_get_reports_by_authority_id(client):
    """Test retrieving reports by authority ID."""
    authority_id = "sample_authority_id"
    response = requests.get(f"{client}/get_reports_by_authority_id/{authority_id}")
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list), "Expected a list of reports"


def test_search_reports_by_description(client):
    """Test searching reports by description."""
    description = "Test report description"
    response = requests.get(
        f"{client}/search/description", params={"description": description}
    )
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list), "Expected a list of reports"


def test_search_reports_by_title(client):
    """Test searching reports by title."""
    title = "Test Report Title"
    response = requests.get(f"{client}/search/title", params={"title": title})
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list), "Expected a list of reports"


def test_submit_report(client):
    """Test submitting a report with image upload."""
    report_data = {
        "user_id": TEST_USER_ID,
        "description": "Submitted report description",
        "title": "Submitted Report Title",
        "longitude": 103.8198,
        "latitude": 1.3521,
        "incident_time": int(time.time()),
    }
    with open(image_path, "rb") as file:
        files = {"image": (image_path, file, "image/png")}
        response = requests.post(
            f"{client}/submit-report/", data=report_data, files=files
        )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["message"] == "Report received successfully"


def test_delete_report(client):
    """Test deleting a report by ID."""
    response = requests.delete(f"{client}/{TEST_REPORT_ID}")
    if response.status_code == status.HTTP_200_OK:
        assert response.json()["detail"] == "Report deleted successfully."
    elif response.status_code == status.HTTP_404_NOT_FOUND:
        assert response.json()["detail"] == "Report not found"


def test_update_report_status(client):
    """Test updating the status of a report."""
    new_status = "Resolved"
    response = requests.put(
        f"{client}/{TEST_REPORT_ID}/status", params={"status": new_status}
    )
    if response.status_code == status.HTTP_200_OK:
        assert response.json()["detail"] == "Report status updated successfully."
    elif response.status_code == status.HTTP_404_NOT_FOUND:
        assert response.json()["detail"] == "Report not found"


def test_get_report_picture(client):
    """Test retrieving the picture of a report."""
    response = requests.get(f"{client}/reportPicture/{TEST_REPORT_ID}")
    if response.status_code == status.HTTP_200_OK:
        assert response.headers["content-type"] in ["image/png", "image/jpeg"]
    elif response.status_code == status.HTTP_404_NOT_FOUND:
        assert response.json()["detail"] == "Report not found"


# phoney cases
def test_get_reports_by_nonexistent_user_id(client):
    """Test retrieving reports for a non-existent user ID."""
    nonexistent_user_id = str(uuid4())  # Generate a random ID
    response = requests.get(f"{client}/user/{nonexistent_user_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "User not found"


def test_read_nonexistent_report_by_id(client):
    """Test retrieving a non-existent report by ID."""
    nonexistent_report_id = str(uuid4())  # Generate a random ID
    response = requests.get(f"{client}/{nonexistent_report_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Report not found"

def test_delete_nonexistent_report(client):
    """Test deleting a non-existent report by ID."""
    nonexistent_report_id = str(uuid4())  # Generate a random ID
    response = requests.delete(f"{client}/{nonexistent_report_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Report not found"

def test_update_nonexistent_report_status(client):
    """Test updating the status of a non-existent report."""
    nonexistent_report_id = str(uuid4())  # Generate a random ID
    new_status = "Resolved"
    response = requests.put(
        f"{client}/{nonexistent_report_id}/status", params={"status": new_status}
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Report not found"


def test_get_nonexistent_report_picture(client):
    """Test retrieving the picture of a non-existent report."""
    nonexistent_report_id = str(uuid4())  # Generate a random ID
    response = requests.get(f"{client}/reportPicture/{nonexistent_report_id}")
    assert response.status_code == status.HTTP_200_OK
