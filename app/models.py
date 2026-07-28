from datetime import datetime
from sqlalchemy import String, Integer, Boolean, DateTime, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from app.db import Base

class City(Base):
    __tablename__ = "cities"

    id: Mapped[int] = mapped_column(primary_key=True)
    ibge_code: Mapped[str] = mapped_column(String(20), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(150), index=True)
    state: Mapped[str] = mapped_column(String(2), index=True)

class Lead(Base):
    __tablename__ = "leads"
    __table_args__ = (
        UniqueConstraint("source", "external_id", name="uq_source_external_id"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    source: Mapped[str] = mapped_column(String(30), default="manual", index=True)
    external_id: Mapped[str | None] = mapped_column(String(255), nullable=True)

    company_name: Mapped[str] = mapped_column(String(255), index=True)
    category: Mapped[str | None] = mapped_column(String(150), nullable=True, index=True)
    city: Mapped[str | None] = mapped_column(String(150), nullable=True, index=True)
    state: Mapped[str | None] = mapped_column(String(2), nullable=True, index=True)
    address: Mapped[str | None] = mapped_column(String(500), nullable=True)

    phone: Mapped[str | None] = mapped_column(String(50), nullable=True)
    whatsapp: Mapped[str | None] = mapped_column(String(50), nullable=True)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    website: Mapped[str | None] = mapped_column(String(500), nullable=True)
    instagram: Mapped[str | None] = mapped_column(String(500), nullable=True)
    facebook: Mapped[str | None] = mapped_column(String(500), nullable=True)
    linkedin: Mapped[str | None] = mapped_column(String(500), nullable=True)
    google_maps_url: Mapped[str | None] = mapped_column(String(700), nullable=True)

    has_website: Mapped[bool] = mapped_column(Boolean, default=False)
    has_ssl: Mapped[bool] = mapped_column(Boolean, default=False)
    is_responsive: Mapped[bool] = mapped_column(Boolean, default=False)
    looks_outdated: Mapped[bool] = mapped_column(Boolean, default=False)
    has_whatsapp_link: Mapped[bool] = mapped_column(Boolean, default=False)
    has_contact_form: Mapped[bool] = mapped_column(Boolean, default=False)

    pagespeed_performance: Mapped[int | None] = mapped_column(Integer, nullable=True)
    pagespeed_accessibility: Mapped[int | None] = mapped_column(Integer, nullable=True)
    pagespeed_seo: Mapped[int | None] = mapped_column(Integer, nullable=True)
    response_ms: Mapped[int | None] = mapped_column(Integer, nullable=True)

    score: Mapped[int] = mapped_column(Integer, default=0, index=True)
    score_reason: Mapped[str | None] = mapped_column(Text, nullable=True)

    status: Mapped[str] = mapped_column(String(30), default="novo", index=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    do_not_contact: Mapped[bool] = mapped_column(Boolean, default=False, index=True)

    last_contact_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    next_followup_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
