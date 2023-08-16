from passlib.context import CryptContext


pwd_context = CryptContext(schemes=['bcrypt'])

from fastapi import HTTPException
from models.xona import Xona

from utils.pagination import pagination


def all_xona(search, status, roll, page, limit, db):
    if search:
        search_formatted = "%{}%".format(search)
        search_filter = Xona.xona_nomi.like(search_formatted) | Xona.raqami.like(search_formatted)
    else:
        search_filter = Xona.id > 0
    if status in [True, False]:
        status_filter = Xona.status == status
    else:
        status_filter = Xona.id > 0

    if roll:
        roll_filter = Xona.fan_id == roll
    else:
        roll_filter = Xona.id > 0

    users = db.query(Xona).filter(search_filter, status_filter, roll_filter).order_by(Xona.xona_nomi.asc())
    if page and limit:
        return pagination(users, page, limit)
    else:
        return users.all()


def one_xona(id, db):
    return db.query(Xona).filter(Xona.id == id).first()


def xona_current(user, db):
    return db.query(Xona).filter(Xona.id == user.id).first()


def create_xona(form, user, db):
    user_verification = db.query(Xona).filter(Xona.xona_nomi == form.xona_nomi).first()
    if user_verification:
        raise HTTPException(status_code=400, detail="Bunday xona_nomi mavjud")
    number_verification = db.query(Xona).filter(Xona.raqami == form.raqami).first()
    if number_verification:
        raise HTTPException(status_code=400, detail="Bunday raqami mavjud")

    new_user_db = Xona(
        xona_nomi=form.xona_nomi,
        raqami=form.raqami,
        user_id=user.id

    )
    db.add(new_user_db)
    db.commit()
    db.refresh(new_user_db)

    return new_user_db


def update_xona(form, user, db):
    if one_xona(form.id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday id raqamli foydalanuvchi mavjud emas")
    user_verification = db.query(Xona).filter(Xona.raqami == form.raqami).first()
    if user_verification and user_verification.id != form.id:
        raise HTTPException(status_code=400, detail="Bunday raqami mavjud")

    db.query(Xona).filter(Xona.id == form.id).update({
        Xona.id: form.id,
        Xona.xona_nomi: form.xona_nomi,
        Xona.raqami: form.raqami,
        Xona.status: form.status,
        Xona.user_id: form.user_id

    })
    db.commit()

    return one_xona(form.id, db)


def update_xona_salary(id, salary, db):
    if one_xona(id, db) is None:
        raise HTTPException(status_code=400, detail=f"Bunday {id} raqamli hodim mavjud emas")

    db.query(Xona).filter(Xona.id == id).update({
        Xona.salary: salary,

    })
    db.commit()
    return one_xona(id, db)


def xona_delete(id, user, db):
    if one_xona(id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday id raqamli ma'lumot mavjud emas")
    db.query(Xona).filter(Xona.id == id).update({
        Xona.status: False,
    })
    db.commit()
    return {"date": "Ma'lumot o'chirildi !"}
