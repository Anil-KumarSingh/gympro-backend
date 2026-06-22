from fastapi import APIRouter
from app.database.mongodb import db

router = APIRouter()

@router.get("/users")
def get_all_users():

    users = list(
        db.users.find(
            {},
            {
                "_id": 0,
                "password": 0
            }
        )
    )

    return users

@router.get("/complaints")
def get_all_complaints():

    complaints = list(
        db.complaints.find(
            {},
            {
                "_id": 0
            }
        )
    )

    return complaints
@router.delete("/user/{email}")
def delete_user(email: str):

    result = db.users.delete_one(
        {"email": email}
    )

    if result.deleted_count == 0:
        return {
            "message": "User not found"
        }

    return {
        "message": "User deleted successfully"
    }