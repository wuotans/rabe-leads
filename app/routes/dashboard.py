from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from sqlalchemy import func, select
from sqlalchemy.orm import Session
from app.db import get_db
from app.models import Lead

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
def dashboard(request: Request, db: Session = Depends(get_db)):
    total = db.scalar(select(func.count()).select_from(Lead)) or 0
    high = db.scalar(select(func.count()).select_from(Lead).where(Lead.score >= 60)) or 0
    no_site = db.scalar(select(func.count()).select_from(Lead).where(Lead.has_website == False)) or 0
    contacted = db.scalar(select(func.count()).select_from(Lead).where(Lead.status != "novo")) or 0
    latest = db.scalars(select(Lead).order_by(Lead.created_at.desc()).limit(10)).all()
    return request.app.state.templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "total": total,
            "high": high,
            "no_site": no_site,
            "contacted": contacted,
            "latest": latest,
        },
    )
