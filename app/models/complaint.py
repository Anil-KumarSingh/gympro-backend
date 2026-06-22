from pydantic import BaseModel

class Complaint(BaseModel):
    subject: str
    message: str