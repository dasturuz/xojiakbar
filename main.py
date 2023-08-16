from db import SessionLocal
from fastapi import FastAPI
from fastapi_utils.tasks import repeat_every
from sqlalchemy.orm import Session

from models import Users
from routes import users, auth, oquvchi, oqtuvchi, tolov, xona, kurslar, kurssanalari, fanlar, chiqimlar
from db import Base, engine
import datetime

from routes.auth import get_password_hash

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Eko zamin",
)

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/')
def home():
    return {"message": "Welcome"}


app.include_router(
    auth.login_router,
    prefix='/auth',
    tags=['User auth section'],
    responses={200: {'description': 'Ok'}, 201: {'description': 'Created'}, 400: {'description': 'Bad Request'},
               401: {'desription': 'Unauthorized'}}
)

app.include_router(
    users.router_user,
    prefix='/user',
    tags=['User section'],
    responses={200: {'description': 'Ok'}, 201: {'description': 'Created'}, 400: {'description': 'Bad Request'},
               401: {'desription': 'Unauthorized'}}
)

app.include_router(
    oquvchi.router_oquvchi,
    prefix='/oquvchi',
    tags=['oquvchi section'],
    responses={200: {'description': 'Ok'}, 201: {'description': 'Created'}, 400: {'description': 'Bad Request'},
               401: {'desription': 'Unauthorized'}}
)

app.include_router(
    oqtuvchi.router_oqtuvchi,
    prefix='/oqtuvchi',
    tags=['oqtuvchi section'],
    responses={200: {'description': 'Ok'}, 201: {'description': 'Created'}, 400: {'description': 'Bad Request'},
               401: {'desription': 'Unauthorized'}}
)

app.include_router(
    tolov.router_tolov,
    prefix='/tolov',
    tags=['tolov section'],
    responses={200: {'description': 'Ok'}, 201: {'description': 'Created'}, 400: {'description': 'Bad Request'},
               401: {'desription': 'Unauthorized'}}
)

app.include_router(
    xona.router_xona,
    prefix='/xona',
    tags=['xona section'],
    responses={200: {'description': 'Ok'}, 201: {'description': 'Created'}, 400: {'description': 'Bad Request'},
               401: {'desription': 'Unauthorized'}}
)

app.include_router(
    kurssanalari.router_kurssanalari,
    prefix='/kurssanalari',
    tags=['kurssanalari section'],
    responses={200: {'description': 'Ok'}, 201: {'description': 'Created'}, 400: {'description': 'Bad Request'},
               401: {'desription': 'Unauthorized'}}
)

app.include_router(
    kurslar.router_kurslar,
    prefix='/kurslar',
    tags=['kurslar section'],
    responses={200: {'description': 'Ok'}, 201: {'description': 'Created'}, 400: {'description': 'Bad Request'},
               401: {'desription': 'Unauthorized'}}
)

app.include_router(
    fanlar.router_fanlar,
    prefix='/fanlar',
    tags=['fanlar section'],
    responses={200: {'description': 'Ok'}, 201: {'description': 'Created'}, 400: {'description': 'Bad Request'},
               401: {'desription': 'Unauthorized'}}
)

app.include_router(
    chiqimlar.router_chiqimlar,
    prefix='/chiqimlar',
    tags=['chiqimlar section'],
    responses={200: {'description': 'Ok'}, 201: {'description': 'Created'}, 400: {'description': 'Bad Request'},
               401: {'desription': 'Unauthorized'}}
)

try:
    db = SessionLocal()
    new_user_db = Users(
        name='Xojiakbar',
        username='xoji',
        number='form.number',
        password=get_password_hash('2008'),
        roll='www',
        status=True,
    )
    db.add(new_user_db)
    db.commit()
    db.refresh(new_user_db)
except Exception:
    print(Exception)
