from fastapi import APIRouter, Depends
from app.database.mongodb import db
from app.utils.auth import verify_token

router = APIRouter()


@router.get("/")
def dashboard(user=Depends(verify_token)):
    """
    Dashboard data for logged-in user.
    """

    email = user["email"]

    # Profile
    profile = db.users.find_one(
        {"email": email},
        {"_id": 0, "password": 0}
    )

    # Workout history
    workouts = list(
        db.workouts.find(
            {"user_email": email},
            {"_id": 0}
        )
    )

    # Workout stats
    total_workouts = len(workouts)
    total_reps = sum(w.get("reps", 0) for w in workouts)
    total_duration = sum(w.get("duration", 0) for w in workouts)

    return {
        "profile": profile,
        "workout_stats": {
            "total_workouts": total_workouts,
            "total_reps": total_reps,
            "total_duration": total_duration
        },
        "recent_workouts": workouts[-5:]
    }