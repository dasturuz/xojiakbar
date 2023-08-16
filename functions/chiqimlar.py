from passlib.context import CryptContext


pwd_context = CryptContext(schemes=['bcrypt'])

from fastapi import HTTPException
from models.chiqimlar import Chiqimlar

from utils.pagination import pagination


def all_chiqimlar(search, status, roll, page, limit, db):
    if search:
        search_formatted = "%{}%".format(search)
        search_filter = Chiqimlar.oqtuvchi_id.like(search_formatted) | Chiqimlar.pul.like(search_formatted)
    else:
        search_filter = Chiqimlar.id > 0
    if status in [True, False]:
        status_filter = Chiqimlar.status == status
    else:
        status_filter = Chiqimlar.id > 0

    if roll:
        roll_filter = Chiqimlar.fan_id == roll
    else:
        roll_filter = Chiqimlar.id > 0

    users = db.query(Chiqimlar).filter(search_filter, status_filter, roll_filter).order_by(Chiqimlar.pul.asc())
    if page and limit:
        return pagination(users, page, limit)
    else:
        return users.all()


def one_chiqimlar(id, db):
    return db.query(Chiqimlar).filter(Chiqimlar.id == id).first()


def chiqimlar_current(user, db):
    return db.query(Chiqimlar).filter(Chiqimlar.id == user.id).first()


def create_chiqimlar(form, user, db):
    user_verification = db.query(Chiqimlar).filter(Chiqimlar.oqtuvchi_id == form.oqtuvchi_id).first()
    if user_verification:
        raise HTTPException(status_code=400, detail="Bunday oqtuvchi_id mavjud")

    new_user_db = Chiqimlar(
        oqtuvchi_id=form.oqtuvchi_id,
        turi=form.turi,
        pul=form.pul,
        comment=form.comment,
        user_id=user.id,
    )
    db.add(new_user_db)
    db.commit()
    db.refresh(new_user_db)

    return new_user_db


def update_chiqimlar(form, user, db):
    if one_chiqimlar(form.id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday id raqamli foydalanuvchi mavjud emas")
    user_verification = db.query(Chiqimlar).filter(Chiqimlar.pul == form.pul).first()
    if user_verification and user_verification.id != form.id:
        raise HTTPException(status_code=400, detail="Bunday pul mavjud")

    db.query(Chiqimlar).filter(Chiqimlar.id == form.id).update({
        Chiqimlar.id: form.id,
        Chiqimlar.oqtuvchi_id: form.oqtuvchi_id,
        Chiqimlar.pul: form.pul,
        Chiqimlar.turi: form.turi,
        Chiqimlar.comment: form.comment,
        Chiqimlar.status: form.status,
        Chiqimlar.user_id: form.user_id

    })
    db.commit()

    return one_chiqimlar(form.id, db)


def update_chiqimlar_salary(id, salary, db):
    if one_chiqimlar(id, db) is None:
        raise HTTPException(status_code=400, detail=f"Bunday {id} raqamli hodim mavjud emas")

    db.query(Chiqimlar).filter(Chiqimlar.id == id).update({
        Chiqimlar.salary: salary,

    })
    db.commit()
    return one_chiqimlar(id, db)


def chiqimlar_delete(id, user, db):
    if one_chiqimlar(id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday id raqamli ma'lumot mavjud emas")
    db.query(Chiqimlar).filter(Chiqimlar.id == id).update({
        Chiqimlar.status: False,
    })
    db.commit()
    return {"date": "Ma'lumot o'chirildi !"}
