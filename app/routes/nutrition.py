from fastapi import APIRouter, Depends
from app.database.mongodb import db
from app.models.nutrition import Nutrition
from app.utils.auth import verify_token

router = APIRouter()


@router.post("/add")
def add_nutrition(
    nutrition: Nutrition,
    user=Depends(verify_token)
):
    """
    Add nutrition entry for logged-in user.
    """

    nutrition_data = {
        "user_email": user["email"],
        "meal_type": nutrition.meal_type,
        "food_name": nutrition.food_name,
        "calories": nutrition.calories,
        "protein": nutrition.protein,
        "carbs": nutrition.carbs,
        "fat": nutrition.fat
    }

    db.nutrition.insert_one(nutrition_data)

    return {
        "message": "Nutrition entry added successfully"
    }
@router.get("/my")
def my_nutrition(
    user=Depends(verify_token)
):
    """
    Get all nutrition entries
    of the logged-in user.
    """

    nutrition = list(
        db.nutrition.find(
            {"user_email": user["email"]},
            {"_id": 0}
        )
    )

    return nutrition

@router.get("/stats")
def nutrition_stats(
    user=Depends(verify_token)
):
    """
    Get nutrition summary
    of logged-in user.
    """

    entries = list(
        db.nutrition.find(
            {"user_email": user["email"]}
        )
    )

    total_calories = sum(
        item.get("calories", 0)
        for item in entries
    )

    total_protein = sum(
        item.get("protein", 0)
        for item in entries
    )

    total_carbs = sum(
        item.get("carbs", 0)
        for item in entries
    )

    total_fat = sum(
        item.get("fat", 0)
        for item in entries
    )

    return {
        "total_meals": len(entries),
        "total_calories": total_calories,
        "total_protein": total_protein,
        "total_carbs": total_carbs,
        "total_fat": total_fat
    }