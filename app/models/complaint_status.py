from pydantic import BaseModel

class ComplaintStatus(BaseModel):
    status: str