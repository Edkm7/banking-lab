from fastapi import FastAPI
from app.api import accounts
from app.db.session import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Accounts Service")

app.include_router(accounts.router)
