import argparse
from sqlalchemy import select
from app.db import SessionLocal
from app.models import Lead
from app.services.site_analyzer import analyze_html, pagespeed
from app.services.scoring import calculate_score

parser = argparse.ArgumentParser()
parser.add_argument("--limit", type=int, default=50)
parser.add_argument("--pagespeed", action="store_true")
args = parser.parse_args()

db = SessionLocal()
try:
    leads = db.scalars(
        select(Lead)
        .where(Lead.do_not_contact == False)
        .order_by(Lead.score.asc(), Lead.created_at.asc())
        .limit(args.limit)
    ).all()

    for lead in leads:
        if lead.website:
            result = analyze_html(lead.website)
            for key, value in result.items():
                if hasattr(lead, key) and value is not None:
                    setattr(lead, key, value)
            if args.pagespeed:
                try:
                    for key, value in pagespeed(lead.website).items():
                        setattr(lead, key, value)
                except Exception as exc:
                    print(f"PageSpeed falhou em {lead.company_name}: {exc}")
        lead.score, lead.score_reason = calculate_score(lead)
        db.commit()
        print(lead.score, lead.company_name, "-", lead.score_reason)
finally:
    db.close()
