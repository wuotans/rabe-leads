import requests
from sqlalchemy import select
from app.db import SessionLocal, Base, engine
from app.models import City

URL = "https://servicodados.ibge.gov.br/api/v1/localidades/municipios"

Base.metadata.create_all(engine)
payload = requests.get(URL, timeout=60).json()
db = SessionLocal()
created = 0
try:
    for item in payload:
        state = item["microrregiao"]["mesorregiao"]["UF"]["sigla"]
        code = str(item["id"])
        if db.scalar(select(City).where(City.ibge_code == code)):
            continue
        db.add(City(ibge_code=code, name=item["nome"], state=state))
        created += 1
    db.commit()
finally:
    db.close()

print(f"{created} municípios adicionados.")
