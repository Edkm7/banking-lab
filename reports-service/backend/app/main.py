from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import reports
from app.core.db import Base, engine
import logging

# create tables if they don't exist (they exist from auth/accounts but safe)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Reports Service")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

app.include_router(reports.router)
