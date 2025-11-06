from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select, Session
from app.core.db import get_session
from app.models import User
from app.schemas import UserCreate, UserRead
from app.core.security import get_password_hash
from typing import List
from app.core.rabbitmq import publish

router = APIRouter()

@router.post("/", response_model=UserRead, status_code=201)
def create_user(payload: UserCreate, session: Session = Depends(get_session)):
    existing = session.exec(select(User).where(User.username == payload.username)).first()
    if existing:
        raise HTTPException(status_code=400, detail="username exists")
    u = User(username=payload.username, email=payload.email, hashed_password=get_password_hash(payload.password))
    session.add(u)
    session.commit()
    session.refresh(u)
    publish(exchange="events", routing_key="user.created", body={"user_id": u.id, "username": u.username, "email": u.email})
    return u

@router.get("/", response_model=List[UserRead])
def list_users(session: Session = Depends(get_session)):
    return session.exec(select(User)).all()

@router.get("/{user_id}", response_model=UserRead)
def get_user(user_id: int, session: Session = Depends(get_session)):
    u = session.get(User, user_id)
    if not u:
        raise HTTPException(status_code=404)
    return u

@router.patch("/{user_id}", response_model=UserRead)
def update_user(user_id: int, payload: UserCreate, session: Session = Depends(get_session)):
    u = session.get(User, user_id)
    if not u:
        raise HTTPException(status_code=404)
    u.username = payload.username
    u.email = payload.email
    u.hashed_password = get_password_hash(payload.password)
    session.add(u)
    session.commit()
    session.refresh(u)
    return u

@router.delete("/{user_id}", status_code=204)
def delete_user(user_id: int, session: Session = Depends(get_session)):
    u = session.get(User, user_id)
    if not u:
        raise HTTPException(status_code=404)
    session.delete(u)
    session.commit()
