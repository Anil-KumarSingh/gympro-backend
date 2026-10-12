from fastapi import APIRouter, Depends
from app.models.bmi import BMI
from app.database.mongodb import db
from app.utils.auth import verify_token

router = APIRouter()

@router.post("/calculate")
def calculate_bmi(
    data: BMI,
    user=Depends(verify_token)
):

    bmi = round(
        data.weight / ((data.height / 100) ** 2),
        2
    )

    if bmi < 18.5:
        category = "Underweight"

    elif bmi < 25:
        category = "Normal"

    elif bmi < 30:
        category = "Overweight"

    else:
        category = "Obese"

    bmi_data = {
        "user_email": user["email"],
        "height": data.height,
        "weight": data.weight,
        "age": data.age,
        "gender": data.gender,
        "bmi": bmi,
        "category": category
    }

    db.bmi.insert_one(bmi_data)

    return {
        "bmi": bmi,
        "category": category
    }
@router.get("/history")
def bmi_history(
    user=Depends(verify_token)
):

    history = list(
        db.bmi.find(
            {"user_email": user["email"]},
            {"_id": 0}
        )
    )

    return history


    


  