from fastapi import FastAPI, Depends
import models
from database import engine
from routers import auth, todos, users, address
from company import companyapis, dependencies

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(
    auth.router,
    prefix="/auth",
    tags=['auth'],
    responses={401: {'user': 'Not Authorized'}}
)
app.include_router(
    todos.router,
    prefix='/todos',
    tags=['todos'],
    responses={404: {"description": "Not found"}}
)
app.include_router(
    users.router,
    prefix="/users",
    tags=['users'],
    responses={404: {"description": "Not found"}}
)
app.include_router(
    address.router,
    prefix="/address",
    tags=['address'],
    responses={404: {"description": "Not found"}}
)
app.include_router(
    companyapis.router,
    prefix="/companyapis",
    tags=['companyapis'],
    dependencies=[Depends(dependencies.get_token_header)],
    responses={418: {"description": "internal use only"}}
)
