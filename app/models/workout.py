from pydantic import BaseModel

class Workout(BaseModel):
    exercise: str
    reps: int
    duration: int