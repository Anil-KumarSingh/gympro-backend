from pydantic import BaseModel, EmailStr

class AdminUser(BaseModel):
    name: str
    email: EmailStr
    role: str
    status: str
    avatar: str