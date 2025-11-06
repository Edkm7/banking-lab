from pydantic import BaseModel
from datetime import datetime

class AccountBase(BaseModel):
    name: str
    balance: float = 0

class AccountCreate(AccountBase):
    pass

class Account(AccountBase):
    id: int
    user_id: int
    created_at: datetime  # <-- modifié

    class Config:
        orm_mode = True
