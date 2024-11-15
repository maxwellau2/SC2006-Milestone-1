import time
from typing import Optional, List, Tuple
from pydantic import BaseModel
import sqlite3
import uuid
from faker import Faker
import random


class Report(BaseModel):
    user_id: str
    relevance: int
    severity: int
    urgency: int
    status: str
    report_id: str
    description: Optional[str]
    image_path: Optional[str]
    title: Optional[str]
    datetime: int
    location: str
    points: int
    ollama_description: str
    authority_id: str = ""


# Database connection
conn = sqlite3.connect("database/reports.db")


def create_report(report: Report) -> Tuple[int, Optional[Report]]:
    """Insert a new report into the Report table."""
    insert_query = """
        INSERT INTO Report (UserID, Relevance, Severity, Urgency, Status, ReportID, Description, imagePath, title, Datetime, Location, Points, OllamaDescription, AuthorityID)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """
    try:
        cursor = conn.cursor()
        cursor.execute(
            insert_query,
            (
                report.user_id,
                report.relevance,
                report.severity,
                report.urgency,
                report.status,
                report.report_id,
                report.description,
                report.image_path,
                report.title,
                report.datetime,
                report.location,
                report.points,
                report.ollama_description,
                report.authority_id,
            ),
        )
        conn.commit()
        return 201, report  # Created
    except sqlite3.IntegrityError as e:
        print(e)
        return 400, None  # Bad request: report_id already exists
    except sqlite3.Error as e:
        print(f"Error inserting report: {e}")
        return 500, None  # Internal server error


fake: Faker = Faker()

predefined_uuids = [
    uuid.UUID("123e4567-e89b-12d3-a456-426614174000"),
    uuid.UUID("123e4567-e89b-12d3-a456-426614174001"),
    uuid.UUID("123e4567-e89b-12d3-a456-426614174002"),
    uuid.UUID("123e4567-e89b-12d3-a456-426614174003"),
    uuid.UUID("123e4567-e89b-12d3-a456-426614174004"),
    uuid.UUID("123e4567-e89b-12d3-a456-426614174005"),
]

predefined_authority_id = [
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


def generate_fake_reports(num_reports: int) -> List[Report]:
    """Generate a list of fake Report entries."""
    reports = []
    status_options = ["Pending", "In Progress", "Resolved"]

    for i in range(num_reports):
        report = Report(
            user_id=str(predefined_uuids[i % len(predefined_uuids)]),
            relevance=fake.random_int(min=1, max=10),
            severity=fake.random_int(min=1, max=10),
            urgency=fake.random_int(min=1, max=10),
            status=random.choice(status_options),
            report_id=str(uuid.uuid4()),
            description=fake.sentence(nb_words=10),
            image_path=fake.file_path(extension="jpg"),
            title=fake.catch_phrase(),
            datetime=int(time.time()),  # Unix timestamp
            location=f"{random.randint(1, 100)}.{random.randint(1, 100)},{random.randint(1, 100)}.{random.randint(1, 100)}",  # Location as a string
            points=random.randint(60, 100),
            ollama_description=fake.catch_phrase(),
            authority_id=str(predefined_authority_id[i % len(predefined_authority_id)]),
        )
        reports.append(report)

    return reports


# Generate 10 fake report entries
fake_reports = generate_fake_reports(10)

for report in fake_reports:
    status_code, _ = create_report(report)
    if status_code != 201:
        print(f"Failed to insert report: {report.report_id}")

# Close the database connection
conn.close()
