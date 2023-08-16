from passlib.context import CryptContext


pwd_context = CryptContext(schemes=['bcrypt'])

from fastapi import HTTPException
from models.kurslar import Kurslar

from utils.pagination import pagination


def all_kurslar(search, status, roll, page, limit, db):
    if search:
        search_formatted = "%{}%".format(search)
        search_filter = Kurslar.oqtuvchi_id.like(search_formatted) | Kurslar.fan_id.like(search_formatted)
    else:
        search_filter = Kurslar.id > 0
    if status in [True, False]:
        status_filter = Kurslar.status == status
    else:
        status_filter = Kurslar.id > 0

    if roll:
        roll_filter = Kurslar.fan_id == roll
    else:
        roll_filter = Kurslar.id > 0

    users = db.query(Kurslar).filter(search_filter, status_filter, roll_filter).order_by(Kurslar.fan_id.asc())
    if page and limit:
        return pagination(users, page, limit)
    else:
        return users.all()


def one_kurslar(id, db):
    return db.query(Kurslar).filter(Kurslar.id == id).first()


def kurslar_current(user, db):
    return db.query(Kurslar).filter(Kurslar.id == user.id).first()


def create_kurslar(form, user, db):
    user_verification = db.query(Kurslar).filter(Kurslar.oqtuvchi_id == form.oqtuvchi_id).first()
    if user_verification:
        raise HTTPException(status_code=400, detail="Bunday oqtuvchi_id mavjud")
    number_verification = db.query(Kurslar).filter(Kurslar.fan_id == form.fan_id).first()
    if number_verification:
        raise HTTPException(status_code=400, detail="Bunday fan_id  mavjud")

    new_user_db = Kurslar(
        oqtuvchi_id=form.oqtuvchi_id,
        fan_id=form.fan_id,
        xona=form.xona,
        kurs_muddati=form.kurs_muddati,
        soat=form.soat,
        user_id=user.id

    )
    db.add(new_user_db)
    db.commit()
    db.refresh(new_user_db)

    return new_user_db


def update_kurslar(form, user, db):
    if one_kurslar(form.id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday id raqamli foydalanuvchi mavjud emas")
    user_verification = db.query(Kurslar).filter(Kurslar.oqtuvchi_id == form.oqtuvchi_id).first()
    if user_verification and user_verification.id != form.id:
        raise HTTPException(status_code=400, detail="Bunday oqtuvchi_id mavjud")

    db.query(Kurslar).filter(Kurslar.id == form.id).update({
        Kurslar.id: form.id,
        Kurslar.oqtuvchi_id: form.oqtuvchi_id,
        Kurslar.fan_id: form.fan_id,
        Kurslar.xona: form.xona,
        Kurslar.kurs_muddati: form.kurs_muddati,
        Kurslar.vaqt: form.vaqt,
        Kurslar.status: form.status,
        Kurslar.user_id: form.user_id

    })
    db.commit()

    return one_kurslar(form.id, db)


def update_kurslar_salary(id, salary, db):
    if one_kurslar(id, db) is None:
        raise HTTPException(status_code=400, detail=f"Bunday {id} raqamli hodim mavjud emas")

    db.query(Kurslar).filter(Kurslar.id == id).update({
        Kurslar.salary: salary,

    })
    db.commit()
    return one_kurslar(id, db)


def kurslar_delete(id, user, db):
    if one_kurslar(id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday id raqamli ma'lumot mavjud emas")
    db.query(Kurslar).filter(Kurslar.id == id).update({
        Kurslar.status: False,
    })
    db.commit()
    return {"date": "Ma'lumot o'chirildi !"}
