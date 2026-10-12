from pydantic import BaseModel

class Nutrition(BaseModel):
    meal_type: str
    food_name: str
    calories: int
    protein: float
    carbs: float
    fat: float