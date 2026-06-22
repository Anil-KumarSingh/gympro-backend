from pydantic import BaseModel, EmailStr
from typing import Optional

class User(BaseModel):
    name: str
    email: EmailStr
    password: str

class UpdateUser(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    height: Optional[float] = None
    weight: Optional[float] = None
    goal: Optional[str] = None