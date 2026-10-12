from pydantic import BaseModel

class Workout(BaseModel):
    workout_name: str
    duration: int
    calories_burned: int