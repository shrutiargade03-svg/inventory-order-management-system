from fastapi import Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.security import get_current_user
from app.models import User

def current_user(user: User = Depends(get_current_user)) -> User:
    return user
