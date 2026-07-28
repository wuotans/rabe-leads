from pydantic import BaseModel, EmailStr
from datetime import datetime


class LeadCreate(BaseModel):
    company_name: str
    category: str | None = None
    city: str | None = None
    state: str | None = None
    phone: str | None = None
    whatsapp: str | None = None
    email: EmailStr | None = None
    website: str | None = None
    instagram: str | None = None
    notes: str | None = None


class LeadUpdate(BaseModel):
    status: str | None = None
    notes: str | None = None
    email: EmailStr | None = None
    whatsapp: str | None = None
    next_followup_at: datetime | None = None
    do_not_contact: bool | None = None
