from pydantic import BaseModel

class BMIRequest(BaseModel):
    height: float  # cm
    weight: float  # kg