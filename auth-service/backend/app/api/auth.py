from fastapi import APIRouter, Depends, HTTPException, status, Body
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import select, Session
from app.core.db import get_session
from app.models import User, RefreshToken
from app.core.security import verify_password, create_access_token, create_refresh_token, decode_token, get_user_id_from_username
from app.schemas import TokenResponse
from datetime import datetime, timezone

router = APIRouter()

@router.post("/login", response_model=TokenResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.username == form_data.username)).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    access = create_access_token(user.username)
    refresh = create_refresh_token(user.username)
    payload = decode_token(refresh)
    exp = datetime.fromtimestamp(payload["exp"], tz=timezone.utc)
    rt = RefreshToken(user_id=user.id, token=refresh, expires_at=exp)
    session.add(rt)
    session.commit()
    return {"access_token": access, "refresh_token": refresh, "token_type": "bearer"}

@router.post("/refresh", response_model=TokenResponse)
def refresh_token(token: str = Body(...), session: Session = Depends(get_session)):
    data = decode_token(token)
    if not data:
        raise HTTPException(status_code=401, detail="Invalid refresh")
    uname = data["sub"]
    rt = session.exec(select(RefreshToken).where(RefreshToken.token == token)).first()
    if not rt:
        raise HTTPException(status_code=401, detail="Refresh token not recognized")
    access = create_access_token(uname)
    refresh = create_refresh_token(uname)
    session.delete(rt)
    session.commit()
    new_exp = datetime.fromtimestamp(decode_token(refresh)["exp"], tz=timezone.utc)
    new_rt = RefreshToken(user_id=rt.user_id, token=refresh, expires_at=new_exp)
    session.add(new_rt)
    session.commit()
    return {"access_token": access, "refresh_token": refresh, "token_type": "bearer"}

@router.post("/logout")
def logout(token: str = Body(...), session: Session = Depends(get_session)):
    rt = session.exec(select(RefreshToken).where(RefreshToken.token == token)).first()
    if rt:
        session.delete(rt)
        session.commit()
    return {"msg": "ok"}
