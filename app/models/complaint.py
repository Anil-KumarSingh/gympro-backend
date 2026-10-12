from pydantic import BaseModel

class Complaint(BaseModel):
    category: str
    subject: str
    description: str