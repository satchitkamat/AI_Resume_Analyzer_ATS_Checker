from pydantic import BaseModel
from datetime import datetime

class ResumeResponse(BaseModel):
    id: int
    filename: str
    orginal_filename: str
    created_at: datetime
    extracted_text: str

    class Config:
        from_attributes = True