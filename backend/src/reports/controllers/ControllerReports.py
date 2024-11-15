import asyncio
import os
import time
from fastapi import APIRouter, File, Form, HTTPException, UploadFile, status
from fastapi.responses import FileResponse, JSONResponse
from typing import Optional
import sqlite3
from PIL import Image
from asyncio import Semaphore
import io
import uuid
from datetime import datetime

from src.reports.models.ReportModels import Report
from src.reports.services.ReportService import ReportService
from src.users.services.UserService import UserService
from src.reports.services.PointsService import PointsService

router = APIRouter(prefix="/reports")
semaphore = Semaphore(1)
# Database connection setup
report_service = ReportService(
    sqlite3.connect("database/reports.db")
)  # Instantiate the ReportService
points_service = PointsService(
    sqlite3.connect("database/users.db"), semaphore
)  # Instantiate the PointsService

IMAGE_SAVE_DIRECTORY = "img/reportimg"


@router.post("/", response_model=Report)
async def create_report(report: Report):
    """Create a new report."""
    status_code, created_report = report_service.create_report(report)
    if status_code == 201:
        return created_report
    elif status_code == 400:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to create report."
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create report.",
        )


@router.get("/user/{user_id}", response_model=list[Report])
async def get_reports_by_user_id(user_id: str):
    """Retrieve all reports submitted by a specific user."""
    status_code, reports = report_service.read_report_by_user_id(user_id)
    if status_code == 404:
        if reports['detail'] == "User not found":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Report not found",
            )
    if status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve reports for the user.",
        )
    return reports


@router.get("/top/{k}/{resolved}", response_model=list[Report])
async def get_top_k_reports_by_severity(k: int, resolved: bool = False):
    """Retrieve top k reports based on severity."""
    status_code, reports = report_service.get_top_k_reports_by_severity(k, resolved)
    if status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve top k reports by severity.",
        )
    return reports


@router.get("/{report_id}", response_model=Optional[Report])
async def read_report_by_id(report_id: str):
    """Retrieve a report by its ID."""
    status_code, report = report_service.read_report_by_id(report_id)
    if status_code == 404:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Report not found"
        )
    elif status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve report.",
        )
    return report


@router.get("/get_reports_by_authority_id/{authority_id}", response_model=list[Report])
async def get_reports_by_authority_id(authority_id: str):
    """Retrieve all reports submitted by a specific user."""
    print("asdasdasdadasdas")
    print(authority_id)
    status_code, reports = report_service.read_report_by_authority_id(authority_id)
    if status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve reports for the user.",
        )
    return reports


@router.get("/search/description", response_model=list[Report])
async def search_reports_by_description(description: str):
    """Search reports by description."""
    status_code, reports = report_service.search_reports_by_description(description)
    if status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to search reports by description.",
        )
    return reports


@router.get("/search/title", response_model=list[Report])
async def search_reports_by_title(title: str):
    """Search reports by title."""
    status_code, reports = report_service.search_reports_by_title(title)
    if status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to search reports by title.",
        )
    return reports


@router.post("/submit-report/")
async def submit_report(
    user_id: str = Form(...),
    description: Optional[str] = Form(None),
    title: Optional[str] = Form(None),
    longitude: Optional[float] = Form(None),
    latitude: Optional[float] = Form(None),
    # location: Optional[str] = Form(None), # location is in the fomat of "lat,long"
    incident_time: Optional[int] = Form(None),
    image: Optional[UploadFile] = File(None),
):
    print(incident_time, longitude, latitude, title, description, user_id)
    # Check if the user exists
    if not report_service.check_user_exists(user_id):
        return JSONResponse(status_code=404, content={"message": "User not found"})
    # Optionally, save or process the image
    if not image:
        return JSONResponse(status_code=400, content={"message": "No image provided"})
    # Read the file contents
    contents = await image.read()

    # generate unique report-id
    report_id = str(uuid.uuid4())

    # Generate a timestamp and create a filename with it
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_extension = image.filename.split(".")[-1]
    unique_filename = f"{report_id}.{file_extension}"
    image_path = os.path.join(IMAGE_SAVE_DIRECTORY, unique_filename)

    # Save the image
    try:
        with open(image_path, "wb") as f:
            f.write(contents)
    except Exception as e:
        print(f"Error saving image: {e}")
        return JSONResponse(
            status_code=500, content={"message": "Failed to save image"}
        )

    print("Image saved at:", image_path)
    # create the new report first
    report = Report(
        user_id=user_id,
        severity=0,
        relevance=0,
        urgency=0,
        status="Pending",
        report_id=report_id,
        description=description,
        image_path=image_path,
        title=title if title else "",
        datetime=incident_time or int(time.time()),
        location=f"{latitude},{longitude}",
    )
    # evalutae report with pointsservice, start the process and return true, do not await
    # asyncio.create_task(points_service.evaluate_and_add_points(user_id, image_path, description))
    asyncio.create_task(points_service.evaluate_and_add_points(report))
    return {"message": "Report received successfully"}


@router.delete("/{report_id}")
async def delete_report(report_id: str):
    """Delete a report by its ID."""
    status_code = report_service.delete_report_by_id(report_id)
    if status_code == 404:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Report not found"
        )
    elif status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete report.",
        )
    return {"detail": "Report deleted successfully."}


@router.put("/{report_id}/status", response_model=dict)
async def update_report_status(report_id: str, status: str):
    """Update the status of a report."""
    status_code = report_service.update_report_status(report_id, status)
    if status_code == 404:
        raise HTTPException(status_code=404, detail="Report not found")
    elif status_code != 200:
        raise HTTPException(
            status_code=500,
            detail="Failed to update report status.",
        )
    return {"detail": "Report status updated successfully."}


@router.get("/reportPicture/{report_id}")
async def get_report_picture(report_id: uuid.UUID):
    """Retrieve the report picture of a report."""
    # Define the path to the images directory
    image_dir = IMAGE_SAVE_DIRECTORY
    # Construct the image file path (assuming .png extension)
    image_path = f"{image_dir}/{report_id}.png"
    default_path = f"{image_dir}/default.png"

    if not os.path.isfile(image_path):
        # try .jpg
        image_path = f"{image_dir}/{report_id}.jpg"

    if not os.path.isfile(image_path):
        # try .jpeg
        image_path = f"{image_dir}/{report_id}.jpeg"

    # Check if the image exists
    if not os.path.isfile(image_path):
        return FileResponse(default_path, media_type="image/png")

    # Return the image file as a response
    return FileResponse(image_path, media_type="image/png")
