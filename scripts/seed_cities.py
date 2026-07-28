import requests
from sqlalchemy import select

from app.db import SessionLocal, Base, engine
from app.models import City

URL = "https://servicodados.ibge.gov.br/api/v1/localidades/municipios"


def extract_state(item: dict) -> str | None:
    immediate_region = item.get("regiao-imediata")
    if immediate_region:
        intermediate_region = immediate_region.get("regiao-intermediaria") or {}
        state = intermediate_region.get("UF") or {}
        if state.get("sigla"):
            return state["sigla"]

    microregion = item.get("microrregiao")
    if microregion:
        mesoregion = microregion.get("mesorregiao") or {}
        state = mesoregion.get("UF") or {}
        if state.get("sigla"):
            return state["sigla"]

    return None


Base.metadata.create_all(engine)

response = requests.get(URL, timeout=60)
response.raise_for_status()
payload = response.json()

db = SessionLocal()
created = 0
updated = 0
ignored = 0

try:
    for item in payload:
        state = extract_state(item)
        code = str(item.get("id", "")).strip()
        name = str(item.get("nome", "")).strip()

        if not state or not code or not name:
            ignored += 1
            print(f"Município ignorado por dados incompletos: {item}")
            continue

        city = db.scalar(select(City).where(City.ibge_code == code))

        if city:
            changed = city.name != name or city.state != state
            city.name = name
            city.state = state
            updated += int(changed)
            continue

        db.add(City(ibge_code=code, name=name, state=state))
        created += 1

    db.commit()
except Exception:
    db.rollback()
    raise
finally:
    db.close()

print(
    f"Carga concluída: {created} municípios adicionados, "
    f"{updated} atualizados e {ignored} ignorados."
)
