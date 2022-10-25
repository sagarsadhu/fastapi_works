import sys

sys.path.append("..")

from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
import models
from database import engine, SessionLocal
from .todos import http_exception, successful_response
from pydantic import BaseModel
from .auth import get_current_user, get_user_exception, get_password_hash, verify_password

router = APIRouter()

models.Base.metadata.create_all(bind=engine)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


class UpdateUser(BaseModel):
    username: str
    password: str
    new_password: str


@router.get("/")
async def get_all_users(db: Session = Depends(get_db)):
    return db.query(models.Users).all()


@router.get("/{user_id}")
async def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.id == user_id).first()

    if user is None:
        raise http_exception()

    return user


@router.get("/read/")
async def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.id == user_id).first()

    if user is None:
        raise http_exception()

    return user


@router.put("/password")
async def change_password(update_user: UpdateUser, user: dict = Depends(get_current_user),
                          db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()

    user_model = db.query(models.Users).filter(models.Users.id == user.get("id")).first()

    if user_model is None:
        raise http_exception()

    if update_user.username == user_model.username and verify_password(update_user.password, user_model.hashed_password):

        hashed_password = get_password_hash(update_user.new_password)
        user_model.hashed_password = hashed_password

        db.add(user_model)
        db.commit()

        return successful_response(200)
    return 'Invalid user or request'


@router.delete("/")
async def delete_user(user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()

    user_model = db.query(models.Users).filter(models.Users.id == user.get("id")).first()

    if user_model is None:
        raise http_exception()

    db.query(models.Todos).filter(models.Todos.owner_id == user.get("id")).delete()
    db.commit()

    db.query(models.Users).filter(models.Users.id == user.get("id")).delete()

    db.commit()

    return successful_response(200)
