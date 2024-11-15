from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from src.users.controllers.ControllerUser import router as user_router
from src.users.controllers.ControllerPublic import router as public_router
from src.reports.controllers.ControllerReports import router as reports_router
from src.rewards.controllers.ControllerReward import router as rewards_router
from src.posts.controllers.ControllerPosts import router as posts_router
import uvicorn

app = FastAPI()


origins = [
    "http://localhost",
    "http://127.0.0.1",
    "http://127.0.0.1/",
    "http://127.0.0.1:5173/",
    "http://127.0.0.1:5173",
    "http://localhost:5173/",
    "http://localhost:5173",
    "http://localhost:8000/",
    "http://localhost:8000",
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# adding more controllers follows this template
# from src.products.ControllerProduct import router as product_router
# app.include_router(product_router, prefix="/products", tags=["products"])


# Include the user router from the users directory
app.include_router(public_router, prefix="/public", tags=["public"])

app.include_router(user_router, prefix="/users", tags=["users"])

app.include_router(reports_router, prefix="/reports", tags=["reports"])

app.include_router(rewards_router, prefix="/rewards", tags=["rewards"])

app.include_router(posts_router, prefix="/posts", tags=["posts"])


@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI application!"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
