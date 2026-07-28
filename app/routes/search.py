from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from app.db import get_db
from app.crud import upsert_google_lead
from app.services.google_places import search_places, normalize_place, GooglePlacesError

router = APIRouter(prefix="/search")


@router.get("", response_class=HTMLResponse)
def form(request: Request):
    return request.app.state.templates.TemplateResponse(
        "search.html", {"request": request, "message": None}
    )


@router.post("", response_class=HTMLResponse)
def run_search(
    request: Request,
    category: str = Form(...),
    city: str = Form(...),
    state: str = Form(...),
    db: Session = Depends(get_db),
):
    query = f"{category} em {city} {state}, Brasil"
    created = 0
    updated = 0
    error = None
    try:
        payload = search_places(query)
        for place in payload.get("places", []):
            _, was_created = upsert_google_lead(
                db, normalize_place(place, category, city, state.upper())
            )
            created += int(was_created)
            updated += int(not was_created)
    except GooglePlacesError as exc:
        error = str(exc)

    message = error or f"Busca concluída: {created} novos e {updated} atualizados."
    return request.app.state.templates.TemplateResponse(
        "search.html", {"request": request, "message": message}
    )
