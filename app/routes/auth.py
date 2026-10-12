from fastapi import APIRouter, HTTPException
from app.models.user import User
from app.models.login import LoginUser
from app.database.mongodb import db
from app.utils.security import (
    hash_password,
    verify_password
)
from app.utils.jwt_handler import create_access_token
from fastapi import Depends
from app.utils.auth import verify_token
from app.models.user import User, UpdateUser
from app.models.complaint import Complaint
from datetime import datetime

router = APIRouter()


@router.post("/signup")
def signup(user: User):

    existing_user = db.users.find_one(
        {"email": user.email}
    )

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    # User data to store in MongoDB
    user_data = {
    "name": user.name,
    "email": user.email,
    "password": hash_password(user.password),

    "role": "user",
    "status": "Active",
    "avatar": f"https://i.pravatar.cc/150?u={user.email}",

    "total_workouts": 0,
    "total_hours": 0,
    "streak": 0,
    "last_login": None
}
    db.users.insert_one(user_data)

    return {
        "message": "User registered successfully"
    }

@router.post("/login")
def login(user: LoginUser):

    db_user = db.users.find_one(
        {"email": user.email}
    )

    if not db_user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if not verify_password(
        user.password,
        db_user["password"]
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid password"
        )

    # Update last login time
    db.users.update_one(
        {"email": user.email},
        {
            "$set": {
                "last_login": datetime.utcnow()
            }
        }
    )

    # Create JWT token
    token = create_access_token(
        {
            "email": db_user["email"],
            "role": db_user.get("role", "user")
        }
    )

    return {
        "message": "Login successful",
        "token": token
    }
@router.get("/profile")
def profile(user=Depends(verify_token)):

    db_user = db.users.find_one(
        {"email": user["email"]},
        {"_id": 0, "password": 0}
    )

    return {
    "name": db_user["name"],
    "email": db_user["email"],
    "role": db_user.get("role"),
    "status": db_user.get("status"),
    "avatar": db_user.get("avatar"),

    "total_workouts": db_user.get("total_workouts", 0),
    "total_hours": db_user.get("total_hours", 0),
    "streak": db_user.get("streak", 0),
    "last_login": db_user.get("last_login")
}

@router.put("/profile")
def update_profile(
    user_data: UpdateUser,
    user=Depends(verify_token)
):

    update_data = {
        k: v
        for k, v in user_data.dict().items()
        if v is not None
    }

    db.users.update_one(
        {"email": user["email"]},
        {"$set": update_data}
    )

    return {
        "message": "Profile updated successfully"
    }
