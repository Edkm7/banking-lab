from app.core.db import engine
from sqlmodel import Session, select
from app.models import Account, User

def handle_user_created(payload: dict):
    # payload: {"user_id": <id>, "username": "...", "email": "..."}
    user_id = payload.get("user_id")
    # create default account for user
    with Session(engine) as session:
        acc = Account(user_id=user_id, name=f"default-{payload.get('username')}", balance=0.0)
        session.add(acc); session.commit()
