from fastapi import Depends, HTTPException, status
from app.core.db import get_session
from app.core.security import decode_token
from sqlmodel import Session, select
from app.models import User
from typing import Annotated

def get_current_user(session: Annotated[Session, Depends(get_session)], token: str = Depends(...)):
    # We expect OAuth2 bearer token; FastAPI will provide token dependency in real usage via OAuth2PasswordBearer
    from fastapi.security import OAuth2PasswordBearer
    oauth2 = OAuth2PasswordBearer(tokenUrl="/auth/login")
    token = oauth2.__call__()
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Could not validate credentials")
    username = payload.get("sub")
    user = session.exec(select(User).where(User.username == username)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return user
