from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.db import SessionLocal
from app.models import Account, User
from app.core.security import get_current_username
from sqlalchemy import func

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/reports/accounts-summary")
def accounts_summary(current_user: str = Depends(get_current_username), db: Session = Depends(get_db)):
    # aggregate: per user => count accounts, sum(balance)
    rows = db.query(
        Account.user_id,
        func.count(Account.id).label("count"),
        func.sum(Account.balance).label("total_balance")
    ).group_by(Account.user_id).all()

    # enrich with username
    result = []
    for user_id, count, total_balance in rows:
        user = db.query(User).filter(User.id == user_id).first()
        username = user.username if user else None
        result.append({
            "user_id": user_id,
            "username": username,
            "account_count": int(count),
            "total_balance": float(total_balance or 0.0)
        })
    return result

@router.get("/reports/accounts")
def list_accounts(current_user: str = Depends(get_current_username), db: Session = Depends(get_db)):
    accounts = db.query(Account).all()
    return [
        {"id": a.id, "user_id": a.user_id, "name": a.name, "balance": float(a.balance), "created_at": a.created_at.isoformat()}
        for a in accounts
    ]
