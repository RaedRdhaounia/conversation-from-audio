from pydantic import BaseModel, EmailStr
from typing import Optional

class ContactRequest(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    description: str
    subject: Optional[str] = "Contact Request"
