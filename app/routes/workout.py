from fastapi import APIRouter, Depends
from app.database.mongodb import db
from app.models.workout import Workout
from app.utils.auth import verify_token

router = APIRouter()
@router.post("/add")
def add_workout(
    workout: Workout,
    user=Depends(verify_token)
):

    workout_data = {
        "user_email": user["email"],
        "exercise": workout.exercise,
        "reps": workout.reps,
        "duration": workout.duration
    }

    db.workouts.insert_one(workout_data)

    return {
        "message": "Workout saved successfully"
    }
@router.get("/history")
def workout_history(
    user=Depends(verify_token)
):

    workouts = list(
        db.workouts.find(
            {"user_email": user["email"]},
            {"_id": 0}
        )
    )

    return workouts
@router.get("/stats")
def workout_stats(
    user=Depends(verify_token)
):

    workouts = list(
        db.workouts.find(
            {"user_email": user["email"]}
        )
    )

    total_workouts = len(workouts)

    total_reps = sum(
        workout.get("reps", 0)
        for workout in workouts
    )

    total_duration = sum(
        workout.get("duration", 0)
        for workout in workouts
    )

    return {
        "total_workouts": total_workouts,
        "total_reps": total_reps,
        "total_duration": total_duration
    }