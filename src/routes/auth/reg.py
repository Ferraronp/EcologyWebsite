from fastapi import APIRouter
from passlib.context import CryptContext
from src.routes.auth.database.models.user_model import User as UserFromDB
from .database import db_session

SECRET_KEY = open('src/routes/auth/key.txt').read().strip()
ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

db_session.global_init("src/routes/auth/database/users.db")
router = APIRouter(tags=['Auth'])


def get_password_hash(password):
    return pwd_context.hash(password)


@router.post("/reg_user")
def create_user(username, email, password):
    db_sess = db_session.create_session()
    user = db_sess.query(UserFromDB).filter(UserFromDB.username == username).first()
    if not (user is None):
        return False
    mail = db_sess.query(UserFromDB).filter(UserFromDB.email == email).first()
    if not (mail is None):
        return False
    if len(password) < 8:
        return False

    user = UserFromDB()
    user.username = username
    user.email = email
    user.password = get_password_hash(password)
    db_sess.add(user)
    db_sess.commit()

    return True
