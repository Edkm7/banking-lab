from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import users, auth
from app.core.db import create_db_and_tables
import logging

app = FastAPI(title="Auth Service")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

@app.on_event("startup")
def on_startup():
    logging.info("Creating DB tables if needed")
    create_db_and_tables()

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(users.router, prefix="/users", tags=["users"])
