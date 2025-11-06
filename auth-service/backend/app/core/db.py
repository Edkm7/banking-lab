from sqlmodel import SQLModel, create_engine, Session
from .config import settings

# Création du moteur
engine = create_engine(settings.DATABASE_URL, echo=False)

# Création des tables
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# Fournir une session SQLModel
def get_session():
    with Session(engine) as session:
        yield session
