from app.db import Base, engine
import app.models  # noqa

Base.metadata.create_all(engine)
print("Banco e tabelas criados com sucesso.")
