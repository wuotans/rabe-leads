from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models import Lead


def upsert_google_lead(db: Session, data: dict) -> tuple[Lead, bool]:
    lead = db.scalar(
        select(Lead).where(
            Lead.source == data["source"],
            Lead.external_id == data["external_id"],
        )
    )
    created = lead is None
    if lead is None:
        lead = Lead(**data)
        db.add(lead)
    else:
        for key, value in data.items():
            if value not in (None, ""):
                setattr(lead, key, value)
    db.commit()
    db.refresh(lead)
    return lead, created
