from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models import Account
from app.schemas import AccountCreate, Account as AccountSchema
from app.core.security import get_current_user, get_user_id_from_username

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/accounts", response_model=list[AccountSchema])
def list_accounts(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    user_id = get_user_id_from_username(current_user["username"], db)
    accounts = db.query(Account).filter(Account.user_id == user_id).all()
    return accounts

@router.post("/accounts", response_model=AccountSchema)
def create_account(
    account: AccountCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user_id = get_user_id_from_username(current_user["username"], db)

    # 🔒 Vérification de doublon
    existing = (
        db.query(Account)
        .filter(Account.user_id == user_id, Account.name == account.name)
        .first()
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Account with name '{account.name}' already exists for this user."
        )

    # ✅ Création du compte
    db_account = Account(user_id=user_id, name=account.name, balance=account.balance)
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account
