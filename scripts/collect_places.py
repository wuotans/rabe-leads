import argparse
from app.db import Base, engine, SessionLocal
from app.crud import upsert_google_lead
from app.services.google_places import search_places, normalize_place

parser = argparse.ArgumentParser()
parser.add_argument("--category", required=True)
parser.add_argument("--city", required=True)
parser.add_argument("--state", required=True)
args = parser.parse_args()

Base.metadata.create_all(engine)
query = f"{args.category} em {args.city} {args.state}, Brasil"
payload = search_places(query)
db = SessionLocal()
try:
    for place in payload.get("places", []):
        lead, created = upsert_google_lead(
            db, normalize_place(place, args.category, args.city, args.state.upper())
        )
        print("NOVO" if created else "ATUALIZADO", lead.company_name)
finally:
    db.close()
