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
        "subject": complaint.subject,
        "message": complaint.message,
        "status": "Pending"
    }

    db.complaints.insert_one(complaint_data)

    return {
        "message": "Complaint submitted successfully"
    }

@router.post("/add")
def add_complaint(
    complaint: Complaint,
    user=Depends(verify_token)
):

    complaint_data = {
        "user_email": user["email"],
        "subject": complaint.subject,
        "message": complaint.message,
        "status": "Pending"
    }

    db.complaints.insert_one(complaint_data)

    return {
        "message": "Complaint submitted successfully"
    }
@router.get("/my")
def my_complaints(
    user=Depends(verify_token)
):

    complaints = list(
        db.complaints.find(
            {"user_email": user["email"]},
            {"_id": 0}
        )
    )

    return complaints