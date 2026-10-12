from pydantic import BaseModel

class BMI(BaseModel):
    height: float
    weight: float
    age: int
    gender: str