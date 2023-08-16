from passlib.context import CryptContext
from sqlalchemy.orm import joinedload

pwd_context = CryptContext(schemes=['bcrypt'])

from fastapi import HTTPException
from models.oquvchi import Oquvchi

from routes.auth import get_password_hash
from utils.pagination import pagination


def all_oquvchi(search, status, roll, page, limit, db):
    if search:
        search_formatted = "%{}%".format(search)
        search_filter = Oquvchi.ism.like(search_formatted) | Oquvchi.tel.like(search_formatted) | Oquvchi.familya.like(
            search_formatted) | Oquvchi.fan.like(search_formatted)
    else:
        search_filter = Oquvchi.id > 0
    if status in [True, False]:
        status_filter = Oquvchi.status == status
    else:
        status_filter = Oquvchi.id > 0

    if roll:
        roll_filter = Oquvchi.fan_id == roll
    else:
        roll_filter = Oquvchi.id > 0

    users = db.query(Oquvchi).filter(search_filter, status_filter, roll_filter).order_by(Oquvchi.ism.asc())
    if page and limit:
        return pagination(users, page, limit)
    else:
        return users.all()


def one_oquvchi(id, db):
    return db.query(Oquvchi).filter(Oquvchi.id == id).first()


def oquvchi_current(user, db):
    return db.query(Oquvchi).filter(Oquvchi.id == user.id).first()


def create_oquvchi(form, user, db):
    user_verification = db.query(Oquvchi).filter(Oquvchi.familya == form.familya).first()
    if user_verification:
        raise HTTPException(status_code=400, detail="Bunday familya mavjud")
    number_verification = db.query(Oquvchi).filter(Oquvchi.tel == form.tel).first()
    if number_verification:
        raise HTTPException(status_code=400, detail="Bunday telefon raqami  mavjud")

    new_user_db = Oquvchi(
        ism=form.ism,
        familya=form.familya,
        tel=form.tel,
        yosh=form.yosh,
        fan=form.fan,
        address=form.address,
        user_id=user.id,
        soat=form.soat,

    )
    db.add(new_user_db)
    db.commit()
    db.refresh(new_user_db)

    return new_user_db


def update_oquvchi(form, user, db):
    if one_oquvchi(form.id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday id raqamli foydalanuvchi mavjud emas")
    user_verification = db.query(Oquvchi).filter(Oquvchi.ism == form.ism).first()
    if user_verification and user_verification.id != form.id:
        raise HTTPException(status_code=400, detail="Bunday ism mavjud")

    db.query(Oquvchi).filter(Oquvchi.id == form.id).update({
        Oquvchi.id: form.id,
        Oquvchi.ism: form.ism,
        Oquvchi.familya: form.familya,
        Oquvchi.tel: form.tel,
        Oquvchi.yosh: form.yosh,
        Oquvchi.fan: form.fan,
        Oquvchi.address: form.address,
        Oquvchi.vaqt: form.vaqt,
        Oquvchi.status: form.status,
        Oquvchi.user_id: form.user_id

    })
    db.commit()

    return one_oquvchi(form.id, db)


def update_oquvchi_salary(id, salary, db):
    if one_oquvchi(id, db) is None:
        raise HTTPException(status_code=400, detail=f"Bunday {id} raqamli hodim mavjud emas")

    db.query(Oquvchi).filter(Oquvchi.id == id).update({
        Oquvchi.salary: salary,

    })
    db.commit()
    return one_oquvchi(id, db)


def oquvchi_delete(id, user, db):
    if one_oquvchi(id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday id raqamli ma'lumot mavjud emas")
    db.query(Oquvchi).filter(Oquvchi.id == id).update({
        Oquvchi.status: False,
    })
    db.commit()
    return {"date": "Ma'lumot o'chirildi !"}
