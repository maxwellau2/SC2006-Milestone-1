from fastapi import APIRouter, File, HTTPException, UploadFile, status
from typing import Optional
import uuid
import sqlite3
from src.rewards.models import MyRewards
from src.rewards.models.RewardModel import Reward, RewardUpdate
from src.rewards.services.RewardService import RewardService
from fastapi.responses import FileResponse, JSONResponse
import os


conn = sqlite3.connect("database/rewards.db")
router = APIRouter(prefix="/rewards")

# Instantiate RewardService (assuming it manages connection and interaction with the database)
reward_service = RewardService(conn)


@router.get("/all", response_model=list[Reward])
async def read_all_rewards():
    """Retrieve all rewards."""
    status_code, rewards = reward_service.read_all_rewards()
    if status_code != 200:
        raise HTTPException(
            status_code=status_code, detail="Failed to retrieve rewards."
        )
    return rewards


@router.get("/{reward_id}", response_model=Optional[Reward])
async def read_reward_by_id(reward_id: str):
    """Retrieve a reward by its ID."""
    status_code, reward = reward_service.read_reward_by_id(reward_id)
    if status_code == 404:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Reward not found"
        )
    elif status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve reward.",
        )
    return reward


@router.post("/")
async def create_reward(
    description: str,
    pointsRequired: int,
    availability: int,
    validity: Optional[int] = 0,
    file: UploadFile = File(...),
):
    """Create a new reward."""
    new_reward = Reward(
        rewardID=str(uuid.uuid4()),
        description=description,
        pointsRequired=pointsRequired,
        validity=validity,
        availability=availability,
    )
    status_code = reward_service.create_reward(new_reward)

    image_dir = "img/voucherimg"
    # Ensure the directory exists
    os.makedirs(image_dir, exist_ok=True)

    # Define the image path based on the identifier and original extension
    file_extension = file.filename.split(".")[-1].lower()
    image_path = os.path.join(image_dir, f"{new_reward.rewardID}.{file_extension}")

    # Save the uploaded file
    try:
        with open(image_path, "wb") as image_file:
            image_file.write(await file.read())
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to save image: {str(e)}",
        )
    if status_code == 201:
        return new_reward
    elif status_code == 400:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to create reward."
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create reward.",
        )


@router.put("/{reward_id}/quantity", response_model=dict)
async def update_reward_quantity(reward_id: str, quantity: int):
    """Update reward quantity."""
    status_code = reward_service.update_reward_availability(reward_id, quantity)
    if status_code == 404:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Reward not found"
        )
    elif status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update reward quantity.",
        )
    return {"detail": "Reward quantity updated successfully."}


@router.get("/{reward_id}/validity", response_model=dict)
async def check_reward_validity(reward_id: str):
    """Check the validity of a reward."""
    status_code, reward = reward_service.read_reward_by_id(reward_id)
    if status_code == 404:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Reward not found"
        )
    elif status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve reward.",
        )

    is_valid = reward.getValidity()
    return {"is_valid": is_valid}


@router.post("/{reward_id}/generate", response_model=dict)
async def generate_encoded_reward(reward_id: str, duration: int):
    """Generate a Base64-encoded reward string with specified duration."""
    status_code, reward = reward_service.read_reward(reward_id)
    if status_code == 404:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Reward not found"
        )
    elif status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve reward.",
        )

    encoded_reward = reward.generateReward(duration)
    return {"encoded_reward": encoded_reward}


@router.post("/decode", response_model=dict)
async def decode_reward(encoded_recipe: str):
    """Decode a Base64-encoded reward string."""
    reward = Reward(
        rewardID="dummy",
        description="dummy",
        pointsRequired=0,
        validity=0,
        availability=0,
    )
    decoded_reward = reward.decodeReward(encoded_recipe)
    return {"decoded_reward": decoded_reward}


@router.delete("/{reward_id}", response_model=dict)
async def delete_reward(reward_id: str):
    """Delete a reward by its ID."""
    status_code = reward_service.delete_reward(reward_id)
    if status_code == 404:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Reward not found"
        )
    elif status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete reward.",
        )
    return {"detail": "Reward deleted successfully."}


@router.delete("/wipe", response_model=dict)
async def wipe_rewards():
    """Wipe all rewards from the database."""
    status_code = reward_service.wipe_all_rewards()
    if status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to wipe rewards.",
        )
    return {"detail": "All rewards wiped successfully."}


@router.get("/{reward_identifier}/image", response_class=FileResponse)
async def get_reward_image(reward_identifier: str):
    """Retrieve the image corresponding to the reward identifier."""
    # Define the path to the images directory
    image_dir = "img/voucherimg"
    print("hello!")
    # Construct the image file path (assuming .png extension)
    # check if reward_id is a png file
    reward_identifier = reward_identifier.lower()
    print(reward_identifier)
    if os.path.isfile(os.path.join(image_dir, f"{reward_identifier}.png")):
        image_path = os.path.join(image_dir, f"{reward_identifier}.png")
    elif "-" in reward_identifier:
        # split the reward identifier by -
        reward_identifier_lhs = reward_identifier.split("-")[0]
        image_path = os.path.join(image_dir, f"{reward_identifier_lhs}.png")
    else:
        image_path = os.path.join(image_dir, f"default.png")

    print(image_path)
    # Check if the image exists
    if not os.path.isfile(image_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Image not found"
        )

    # Return the image file
    return FileResponse(image_path, media_type="image/png")


@router.post("/{reward_identifier}/image", response_class=JSONResponse)
async def upload_reward_image(reward_identifier: str, file: UploadFile = File(...)):
    """Upload an image corresponding to the reward identifier."""
    # Define the path to the images directory
    image_dir = "img/voucherimg"
    # Ensure the directory exists
    os.makedirs(image_dir, exist_ok=True)

    # Define the image path based on the identifier and original extension
    file_extension = file.filename.split(".")[-1].lower()
    image_path = os.path.join(image_dir, f"{reward_identifier}.{file_extension}")

    # Save the uploaded file
    try:
        with open(image_path, "wb") as image_file:
            image_file.write(await file.read())
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to save image: {str(e)}",
        )

    return {"detail": "Image uploaded successfully.", "path": image_path}


@router.get("/myrewards/{user_id}")
async def get_my_rewards(user_id: str):
    """Retrieve all rewards submitted by a specific user."""
    status_code, rewards = reward_service.get_user_rewards(user_id)
    if status_code != 200:
        raise HTTPException(
            status_code=status_code, detail="Failed to retrieve rewards."
        )
    return rewards


@router.post("/claim/{reward_id}", response_model=dict)
async def claim_reward(reward_id: str, user_id: str):
    """Claim a reward by its identifier."""
    status_code, reward = reward_service.claim_reward_by_id(reward_id, user_id)
    if status_code == 404:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Reward not found"
        )
    elif status_code == 403:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Insuffient points"
        )
    elif status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to claim reward.",
        )
    return {"detail": "Reward claimed successfully."}


@router.put("/update/{reward_id}", response_model=dict)
async def update_reward(reward_id: str, reward: RewardUpdate):
    """Update a reward by its identifier."""
    status_code = reward_service.update_reward(reward_id, reward)
    if status_code == 404:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Reward not found"
        )
    if status_code == 403:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Insuffient points"
        )
    elif status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update reward.",
        )
    return {"detail": "Reward updated successfully."}
