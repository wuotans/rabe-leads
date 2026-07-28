from datetime import datetime
import csv
import io

from fastapi import APIRouter, Depends, Form, Request, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse, StreamingResponse
from sqlalchemy import select, or_
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import Lead
from app.services.templates import email_subject, email_body, whatsapp_body, whatsapp_link

router = APIRouter(prefix="/leads")


@router.get("", response_class=HTMLResponse)
def list_leads(
    request: Request,
    q: str = "",
    state: str = "",
    status: str = "",
    min_score: int = 0,
    db: Session = Depends(get_db),
):
    stmt = select(Lead).order_by(Lead.score.desc(), Lead.created_at.desc())
    if q:
        stmt = stmt.where(or_(
            Lead.company_name.ilike(f"%{q}%"),
            Lead.city.ilike(f"%{q}%"),
            Lead.category.ilike(f"%{q}%"),
        ))
    if state:
        stmt = stmt.where(Lead.state == state.upper())
    if status:
        stmt = stmt.where(Lead.status == status)
    if min_score:
        stmt = stmt.where(Lead.score >= min_score)
    leads = db.scalars(stmt.limit(500)).all()
    return request.app.state.templates.TemplateResponse(
        "leads.html",
        {
            "request": request,
            "leads": leads,
            "q": q,
            "state": state,
            "status": status,
            "min_score": min_score,
        },
    )


@router.get("/export.csv")
def export_csv(db: Session = Depends(get_db)):
    leads = db.scalars(select(Lead).order_by(Lead.score.desc())).all()
    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerow([
        "Empresa", "Categoria", "Cidade", "Estado", "Site", "E-mail",
        "WhatsApp", "Instagram", "Score", "Status", "Observação"
    ])
    for lead in leads:
        writer.writerow([
            lead.company_name, lead.category, lead.city, lead.state, lead.website,
            lead.email, lead.whatsapp, lead.instagram, lead.score, lead.status, lead.notes
        ])
    content = buffer.getvalue().encode("utf-8-sig")
    return StreamingResponse(
        iter([content]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=rabe_leads.csv"},
    )


@router.get("/{lead_id}", response_class=HTMLResponse)
def detail(request: Request, lead_id: int, db: Session = Depends(get_db)):
    lead = db.get(Lead, lead_id)
    if not lead:
        raise HTTPException(404, "Lead não encontrado")
    return request.app.state.templates.TemplateResponse(
        "lead_detail.html",
        {
            "request": request,
            "lead": lead,
            "email_subject": email_subject(lead),
            "email_body": email_body(lead),
            "whatsapp_body": whatsapp_body(lead),
            "whatsapp_link": whatsapp_link(lead),
        },
    )


@router.post("/{lead_id}/update")
def update(
    lead_id: int,
    status: str = Form(...),
    notes: str = Form(""),
    email: str = Form(""),
    whatsapp: str = Form(""),
    next_followup_at: str = Form(""),
    do_not_contact: str | None = Form(None),
    db: Session = Depends(get_db),
):
    lead = db.get(Lead, lead_id)
    if not lead:
        raise HTTPException(404, "Lead não encontrado")
    lead.status = status
    lead.notes = notes or None
    lead.email = email or None
    lead.whatsapp = whatsapp or None
    lead.do_not_contact = bool(do_not_contact)
    lead.next_followup_at = datetime.fromisoformat(next_followup_at) if next_followup_at else None
    if status != "novo":
        lead.last_contact_at = datetime.utcnow()
    db.commit()
    return RedirectResponse(f"/leads/{lead_id}", status_code=303)
