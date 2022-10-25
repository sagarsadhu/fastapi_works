import sys

sys.path.append("..")

from datetime import datetime, timedelta
from typing import Optional

import models
from database import SessionLocal, engine
from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy.orm import Session

from constants import AuthConstants

SECRET_KEY = AuthConstants.SECRET_KEY
ALGORITHM = AuthConstants.ALGORITHM


class CreateUser(BaseModel):
    username: str
    email: Optional[str]
    first_name: str
    last_name: str
    password: str


bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

models.Base.metadata.create_all(bind=engine)

oauth2bearer = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter()


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_password_hash(password):
    return bcrypt_context.hash(password)


def verify_password(plain_password, hashed_password):
    return bcrypt_context.verify(plain_password, hashed_password)


def authenticate_user(username: str, password: str, db):
    user = db.query(models.Users).filter(models.Users.username == username).first()

    if user is None:
        return False

    if verify_password(password, user.hashed_password) is False:
        return False

    return user


def create_access_token(
        username: str, user_id: int, expires_delta: Optional[timedelta] = None
):
    encode = {"sub": username, "id": user_id}
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=55)
    encode.update({"exp": expire})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: str = Depends(oauth2bearer)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")  # type: ignore
        user_id: int = payload.get("id")  # type: ignore

        if user_id is None or username is None:
            raise get_user_exception()
        return {"username": username, "id": user_id}
    except JWTError as error:
        print(error)
        raise get_user_exception()


@router.post("/create/user")
async def create_new_user(create_user: CreateUser, db: Session = Depends(get_db)):
    create_user_model = models.Users()
    create_user_model.email = create_user.email  # type: ignore
    create_user_model.username = create_user.username  # type: ignore
    create_user_model.first_name = create_user.first_name  # type: ignore
    create_user_model.last_name = create_user.last_name  # type: ignore

    hash_password = get_password_hash(create_user.password)

    create_user_model.hashed_password = hash_password  # type: ignore
    create_user_model.is_active = True  # type: ignore

    db.add(create_user_model)
    db.commit()

    return {"status_code": 201, "detail": "User was created successfully"}


@router.post("/token")
async def login_for_access_token(
        form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = authenticate_user(form_data.username, form_data.password, db)

    if user is False:
        raise token_exception()

    token_expires = timedelta(minutes=60)
    token = create_access_token(user.username, user.id, expires_delta=token_expires)

    return {"token": token}


# Exceptions
def get_user_exception():
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return credentials_exception


def token_exception():
    token_exception_response = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return token_exception_response
