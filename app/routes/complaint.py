from fastapi import APIRouter, Depends
from app.database.mongodb import db
from app.models.complaint import Complaint
from app.utils.auth import verify_token

router = APIRouter()


@router.post("/add")
def add_complaint(
    complaint: Complaint,
    user=Depends(verify_token)
):

    complaint_data = {
        "user_email": user["email"],
        "category": complaint.category,
        "subject": complaint.subject,
        "description": complaint.description,
        "status": "Pending"
    }

    result = db.complaints.insert_one(
        complaint_data
    )

    return {
        "message": "Complaint submitted successfully",
        "complaint_id": str(result.inserted_id)
    }


@router.get("/my")
def my_complaints(
    user=Depends(verify_token)
):

    complaints = []

    for complaint in db.complaints.find(
        {"user_email": user["email"]}
    ):
        complaint["_id"] = str(
            complaint["_id"]
        )

        complaints.append(
            complaint
        )

    return complaints