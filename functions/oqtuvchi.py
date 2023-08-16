from passlib.context import CryptContext
from sqlalchemy.orm import joinedload

pwd_context = CryptContext(schemes=['bcrypt'])

from fastapi import HTTPException
from models.oqtuvchi import Oqtuvchi

from routes.auth import get_password_hash
from utils.pagination import pagination


def all_oqtuvchi(search, status, roll, page, limit, db):
    if search:
        search_formatted = "%{}%".format(search)
        search_filter = Oqtuvchi.ism.like(search_formatted) | Oqtuvchi.tel.like(search_formatted) | Oqtuvchi.familya.like(
            search_formatted) | Oqtuvchi.fan_id.like(search_formatted)
    else:
        search_filter = Oqtuvchi.id > 0
    if status in [True, False]:
        status_filter = Oqtuvchi.status == status
    else:
        status_filter = Oqtuvchi.id > 0

    if roll:
        roll_filter = Oqtuvchi.fan_id == roll
    else:
        roll_filter = Oqtuvchi.id > 0

    users = db.query(Oqtuvchi).filter(search_filter, status_filter, roll_filter).order_by(Oqtuvchi.ism.asc())
    if page and limit:
        return pagination(users, page, limit)
    else:
        return users.all()


def one_oqtuvchi(id, db):
    return db.query(Oqtuvchi).filter(Oqtuvchi.id == id).first()


def oqtuvchi_current(user, db):
    return db.query(Oqtuvchi).filter(Oqtuvchi.id == user.id).first()


def create_oqtuvchi(form, user, db):
    user_verification = db.query(Oqtuvchi).filter(Oqtuvchi.ism == form.ism).first()
    if user_verification:
        raise HTTPException(status_code=400, detail="Bunday ism mavjud")
    number_verification = db.query(Oqtuvchi).filter(Oqtuvchi.tel == form.tel).first()
    if number_verification:
        raise HTTPException(status_code=400, detail="Bunday tel mavjud")

    new_user_db = Oqtuvchi(
        ism=form.ism,
        familya=form.familya,
        tel=form.tel,
        fan_id=form.fan_id,
        password=form.password,
        user_id=user.id,
        roll=form.roll,
        username=form.username
    )
    db.add(new_user_db)
    db.commit()
    db.refresh(new_user_db)

    return new_user_db


def update_oqtuvchi(form, user, db):
    if one_oqtuvchi(form.id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday id raqamli foydalanuvchi mavjud emas")
    user_verification = db.query(Oqtuvchi).filter(Oqtuvchi.familya == form.familya).first()
    if user_verification and user_verification.id != form.id:
        raise HTTPException(status_code=400, detail="Bunday familya mavjud")

    db.query(Oqtuvchi).filter(Oqtuvchi.id == form.id).update({
        Oqtuvchi.id: form.id,
        Oqtuvchi.ism: form.ism,
        Oqtuvchi.familya: form.familya,
        Oqtuvchi.tel: form.tel,
        Oqtuvchi.fan_id: form.fan_id,
        Oqtuvchi.password: form.password,
        Oqtuvchi.status: form.status,
        Oqtuvchi.user_id: form.user_id,
        Oqtuvchi.roll:form.roll,
        Oqtuvchi.username:form.username

    })
    db.commit()

    return one_oqtuvchi(form.id, db)


def update_oqtuvchi_salary(id, salary, db):
    if one_oqtuvchi(id, db) is None:
        raise HTTPException(status_code=400, detail=f"Bunday {id} raqamli hodim mavjud emas")

    db.query(Oqtuvchi).filter(Oqtuvchi.id == id).update({
        Oqtuvchi.salary: salary,

    })
    db.commit()
    return one_oqtuvchi(id, db)


def oqtuvchi_delete(id, user, db):
    if one_oqtuvchi(id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday id raqamli ma'lumot mavjud emas")
    db.query(Oqtuvchi).filter(Oqtuvchi.id == id).update({
        Oqtuvchi.status: False,
    })
    db.commit()
    return {"date": "Ma'lumot o'chirildi !"}
