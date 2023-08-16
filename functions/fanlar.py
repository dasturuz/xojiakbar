from passlib.context import CryptContext


pwd_context = CryptContext(schemes=['bcrypt'])

from fastapi import HTTPException
from models.fanlar import Fanlar

from utils.pagination import pagination


def all_fanlar(search, status, roll, page, limit, db):
    if search:
        search_formatted = "%{}%".format(search)
        search_filter = Fanlar.nomi.like(search_formatted)
    else:
        search_filter = Fanlar.id > 0
    if status in [True, False]:
        status_filter = Fanlar.status == status
    else:
        status_filter = Fanlar.id > 0

    if roll:
        roll_filter = Fanlar.fan_id == roll
    else:
        roll_filter = Fanlar.id > 0

    users = db.query(Fanlar).filter(search_filter, status_filter, roll_filter).order_by(Fanlar.nomi.asc())
    if page and limit:
        return pagination(users, page, limit)
    else:
        return users.all()


def one_fanlar(id, db):
    return db.query(Fanlar).filter(Fanlar.id == id).first()


def fanlar_current(user, db):
    return db.query(Fanlar).filter(Fanlar.id == user.id).first()


def create_fanlar(form, user, db):
    user_verification = db.query(Fanlar).filter(Fanlar.nomi == form.nomi).first()
    if user_verification:
        raise HTTPException(status_code=400, detail="Bunday nomi mavjud")

    new_user_db = Fanlar(
        nomi=form.nomi,
        user_id=user.id,
    )
    db.add(new_user_db)
    db.commit()
    db.refresh(new_user_db)

    return new_user_db


def update_fanlar(form, user, db):
    if one_fanlar(form.id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday id raqamli foydalanuvchi mavjud emas")
    user_verification = db.query(Fanlar).filter(Fanlar.nomi == form.nomi).first()
    if user_verification and user_verification.id != form.id:
        raise HTTPException(status_code=400, detail="Bunday nomi mavjud")

    db.query(Fanlar).filter(Fanlar.id == form.id).update({
        Fanlar.id: form.id,
        Fanlar.nomi: form.nomi,
        Fanlar.status: form.status,
        Fanlar.user_id: form.user_id

    })
    db.commit()

    return one_fanlar(form.id, db)


def update_fanlar_salary(id, salary, db):
    if one_fanlar(id, db) is None:
        raise HTTPException(status_code=400, detail=f"Bunday {id} raqamli hodim mavjud emas")

    db.query(Fanlar).filter(Fanlar.id == id).update({
        Fanlar.salary: salary,

    })
    db.commit()
    return one_fanlar(id, db)


def fanlar_delete(id, user, db):
    if one_fanlar(id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday id raqamli ma'lumot mavjud emas")
    db.query(Fanlar).filter(Fanlar.id == id).update({
        Fanlar.status: False,
    })
    db.commit()
    return {"date": "Ma'lumot o'chirildi !"}
