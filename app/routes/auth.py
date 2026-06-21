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

    user_data = {
        "name": user.name,
        "email": user.email,
        "password": hash_password(user.password)
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

    token = create_access_token(
        {"email": db_user["email"]}
    )

    return {
        "message": "Login successful",
        "token": token
    }

@router.get("/profile")
def profile(user=Depends(verify_token)):

    db_user = db.users.find_one(
        {"email": user["email"]}
    )

    return {
        "name": db_user["name"],
        "email": db_user["email"]
    }