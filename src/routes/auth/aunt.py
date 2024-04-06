from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from passlib.context import CryptContext

from src.routes.auth.database.models.user_model import User as UserFromDB
from .database import db_session

SECRET_KEY = open('src/routes/auth/key.txt').read().strip()
ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

db_session.global_init("src/routes/auth/database/users.db")
router = APIRouter(tags=["Auth"])

security = HTTPBasic()


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_auth_user_username(credentials: Annotated[HTTPBasicCredentials, Depends(security)]) -> str:
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid username or password",
        headers={"WWW-Authenticate": "Basic"}
    )
    db_sess = db_session.create_session()
    user = db_sess.query(UserFromDB).filter(UserFromDB.username == credentials.username).first()

    if user is None:
        raise unauthed_exc

    if not verify_password(credentials.password, user.password):
        raise unauthed_exc

    return credentials.username


@router.post("/basic-auth")
def basic_auth_username(auth_username: str = Depends(get_auth_user_username)):
    return {
        "message": f"Hi, {auth_username}!",
        "username": auth_username,
    }
