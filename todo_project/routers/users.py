import sys

sys.path.append("..")

from starlette.responses import RedirectResponse
from starlette import status

from fastapi import Depends, APIRouter, Request, Form
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from .auth import get_current_user, verify_password, get_password_hash

from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()

models.Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="templates")


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@router.get("/change-password", response_class=HTMLResponse)
async def change_password(request: Request):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)
    return templates.TemplateResponse('change-password.html', {'request': request, 'user': user})


@router.post("/change-password", response_class=HTMLResponse)
async def change_password_user(request: Request, email: str = Form(...), password: str = Form(...),
                               password2: str = Form(...), db: Session = Depends(get_db)):
    user = await get_current_user(request)
    if user is None:
        if user is None:
            return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)

    user_model = db.query(models.Users).filter(models.Users.username == email).first()

    if user_model is None or verify_password(password, user_model.hashed_password) is False:
        msg = "Incorrect Username or Password"
        return templates.TemplateResponse("change-password.html", {"request": request, 'user': user, "msg": msg})

    hash_password = get_password_hash(password2)

    user_model.hashed_password = hash_password

    db.add(user_model)
    db.commit()

    msg = "Password Changed Successfully"
    response = templates.TemplateResponse('login.html', {"request": request, "msg": msg})
    response.delete_cookie("access_token")
    return response
