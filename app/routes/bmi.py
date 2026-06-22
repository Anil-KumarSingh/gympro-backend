from fastapi import APIRouter
from app.models.bmi import BMIRequest

router = APIRouter()

@router.post("/calculate")
def calculate_bmi(data: BMIRequest):

    height_m = data.height / 100

    bmi = data.weight / (height_m ** 2)

    category = ""

    if bmi < 18.5:
        category = "Underweight"
    elif bmi < 25:
        category = "Normal Weight"
    elif bmi < 30:
        category = "Overweight"
    else:
        category = "Obese"

    return {
        "bmi": round(bmi, 2),
        "category": category
    }