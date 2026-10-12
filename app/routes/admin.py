from fastapi import APIRouter, Depends
from app.database.mongodb import db
from app.utils.admin import verify_admin
from app.models.complaint_status import ComplaintStatus
from bson import ObjectId
from fastapi import HTTPException
from app.models.admin_user import AdminUser
from app.utils.security import hash_password
from app.models.admin_user import AdminUser
from app.models.admin_user import AdminUser

router = APIRouter()


@router.get("/users")
def get_all_users(
    admin=Depends(verify_admin)
):
    """
    Fetch all registered users.
    Accessible only by admins.
    """

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
def get_all_complaints(
    admin=Depends(verify_admin)
):
    """
    Get all complaints.
    Admin only.
    """

    complaints = list(
        db.complaints.find({})
    )

    # Convert ObjectId to string
    for complaint in complaints:
        complaint["_id"] = str(complaint["_id"])

    return complaints

@router.delete("/user/{email}")
def delete_user(
    email: str,
    admin=Depends(verify_admin)
):
    """
    Delete a user by email.
    Accessible only by admins.
    """

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

@router.get("/stats")
def admin_stats(
    admin=Depends(verify_admin)
):
    """
    Dashboard statistics for admin.
    """

    total_users = db.users.count_documents({})

    total_workouts = db.workouts.count_documents({})

    total_complaints = db.complaints.count_documents({})

    total_nutrition = db.nutrition.count_documents({})

    total_bmi_records = db.bmi.count_documents({})

    return {
        "total_users": total_users,
        "total_workouts": total_workouts,
        "total_complaints": total_complaints,
        "total_nutrition_entries": total_nutrition,
        "total_bmi_records": total_bmi_records
    }
@router.patch("/complaint/{complaint_id}")
def update_complaint_status(
    complaint_id: str,
    data: ComplaintStatus,
    admin=Depends(verify_admin)
):
    """
    Update complaint status.
    Admin only.
    """

    result = db.complaints.update_one(
        {"_id": ObjectId(complaint_id)},
        {
            "$set": {
                "status": data.status
            }
        }
    )

    if result.modified_count == 0:
        return {
            "message": "Complaint not found"
        }

    return {
        "message": "Complaint status updated successfully"
    }
@router.post("/user")
def create_user(
    user: AdminUser,
    admin=Depends(verify_admin)
):
    """
    Create a new user.
    Admin only.
    """

    existing_user = db.users.find_one(
        {"email": user.email}
    )

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    user_data = {
        "name": user.name,
        "email": user.email,
        "password": hash_password("123456"),
        "role": user.role,
        "status": user.status,
        "avatar": user.avatar
    }

    result = db.users.insert_one(
        user_data
    )

    return {
        "message": "User created successfully",
        "user_id": str(result.inserted_id)
    }

@router.get("/user/{email}")
def get_user_details(
    email: str,
    admin=Depends(verify_admin)
):
    """
    Get complete details of one user.
    """

    user = db.users.find_one(
        {"email": email},
        {"password": 0}
    )

    if not user:
        return {
            "message": "User not found"
        }

    total_workouts = db.workouts.count_documents(
        {"user_email": email}
    )

    workouts = list(
        db.workouts.find(
            {"user_email": email}
        )
    )

    total_duration = sum(
        workout.get("duration", 0)
        for workout in workouts
    )

    user["_id"] = str(user["_id"])

    return {
        "user": user,
        "total_workouts": total_workouts,
        "total_hours": round(
            total_duration / 60,
            2
        ),
        "streak": 0,
        "last_login": user.get(
            "last_login",
            "N/A"
        )
    }
@router.post("/user")
def create_user(
    user: AdminUser,
    admin=Depends(verify_admin)
):

    existing = db.users.find_one(
        {"email": user.email}
    )

    if existing:
        return {
            "message": "Email already exists"
        }

    db.users.insert_one({
        "name": user.name,
        "email": user.email,

        "password": "",

        "role": user.role,
        "status": user.status,
        "avatar": user.avatar,

        "totalWorkouts": 0,
        "totalHours": 0,
        "streak": 0,
        "isActive": True,
        "lastLogin": None
    })

    return {
        "message": "User created successfully"
    }

@router.get("/user/{email}")
def get_user_details(
    email: str,
    admin=Depends(verify_admin)
):

    user = db.users.find_one(
        {"email": email},
        {"password": 0}
    )

    if not user:
        return {
            "message": "User not found"
        }

    user["_id"] = str(user["_id"])

    return user
@router.get("/user/{email}")
def get_user_details(
    email: str,
    admin=Depends(verify_admin)
):
    user = db.users.find_one(
        {"email": email},
        {"password": 0}
    )

    if not user:
        return {"message": "User not found"}

    user["_id"] = str(user["_id"])

    return user

@router.post("/user/add")
def add_user(
    user: AdminUser,
    admin=Depends(verify_admin)
):
    existing_user = db.users.find_one(
        {"email": user.email}
    )

    if existing_user:
        return {
            "message": "User already exists"
        }

    user_data = {
        "name": user.name,
        "email": user.email,
        "role": user.role,
        "status": user.status,
        "avatar": user.avatar,

        "total_workouts": 0,
        "total_hours": 0,
        "streak": 0,
        "last_login": None
    }

    db.users.insert_one(user_data)

    return {
        "message": "User created successfully"
    }

@router.get("/user/{email}")
def get_user_details(
    email: str,
    admin=Depends(verify_admin)
):
    user = db.users.find_one(
        {"email": email},
        {"password": 0}
    )

    if not user:
        return {
            "message": "User not found"
        }

    user["_id"] = str(user["_id"])

    return user

@router.get("/dashboard")
def admin_dashboard(
    admin=Depends(verify_admin)
):
    total_users = db.users.count_documents({})

    active_users = db.users.count_documents(
        {"status": "Active"}
    )

    total_workouts = db.workouts.count_documents({})

    total_complaints = db.complaints.count_documents({})

    return {
        "total_users": total_users,
        "active_users": active_users,
        "new_today": 0,  # implement later
        "total_workouts": total_workouts,
        "total_complaints": total_complaints
    }