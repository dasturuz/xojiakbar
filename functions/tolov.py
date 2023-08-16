from passlib.context import CryptContext


pwd_context = CryptContext(schemes=['bcrypt'])

from fastapi import HTTPException
from models.tolov import Tolov

from utils.pagination import pagination


def all_tolov(search, status, roll, page, limit, db):
    if search:
        search_formatted = "%{}%".format(search)
        search_filter = Tolov.oquvchi_id.like(search_formatted) | Tolov.oy.like(search_formatted) | Tolov.narx.like(
            search_formatted) | Tolov.fan_id.like(search_formatted)
    else:
        search_filter = Tolov.id > 0
    if status in [True, False]:
        status_filter = Tolov.status == status
    else:
        status_filter = Tolov.id > 0

    if roll:
        roll_filter = Tolov.fan_id == roll
    else:
        roll_filter = Tolov.id > 0

    users = db.query(Tolov).filter(search_filter, status_filter, roll_filter).order_by(Tolov.oquvchi_id.asc())
    if page and limit:
        return pagination(users, page, limit)
    else:
        return users.all()


def one_tolov(id, db):
    return db.query(Tolov).filter(Tolov.id == id).first()


def tolov_current(user, db):
    return db.query(Tolov).filter(Tolov.id == user.id).first()


def create_tolov(form, user, db):
    user_verification = db.query(Tolov).filter(Tolov.oquvchi_id == form.oquvchi_id).first()
    if user_verification:
        raise HTTPException(status_code=400, detail="Bunday oquvchi_id mavjud")
    number_verification = db.query(Tolov).filter(Tolov.oy == form.oy).first()
    if number_verification:
        raise HTTPException(status_code=400, detail="Bunday oy  mavjud")

    new_user_db = Tolov(
        oquvchi_id=form.oquvchi_id,
        fan_id=form.fan_id,
        oy=form.oy,
        narx=form.narx,
        turi=form.turi,
        user_id=user.id

    )
    db.add(new_user_db)
    db.commit()
    db.refresh(new_user_db)

    return new_user_db


def update_tolov(form, user, db):
    if one_tolov(form.id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday id raqamli foydalanuvchi mavjud emas")
    user_verification = db.query(Tolov).filter(Tolov.narx == form.narx).first()
    if user_verification and user_verification.id != form.id:
        raise HTTPException(status_code=400, detail="Bunday narx mavjud")

    db.query(Tolov).filter(Tolov.id == form.id).update({
        Tolov.id: form.id,
        Tolov.oquvchi_id: form.oquvchi_id,
        Tolov.fan_id: form.fan_id,
        Tolov.oy: form.oy,
        Tolov.narx: form.narx,
        Tolov.turi: form.turi,
        Tolov.status: form.status,
        Tolov.user_id: form.user_id

    })
    db.commit()

    return one_tolov(form.id, db)


def update_tolov_salary(id, salary, db):
    if one_tolov(id, db) is None:
        raise HTTPException(status_code=400, detail=f"Bunday {id} raqamli hodim mavjud emas")

    db.query(Tolov).filter(Tolov.id == id).update({
        Tolov.salary: salary,

    })
    db.commit()
    return one_tolov(id, db)


def tolov_delete(id, user, db):
    if one_tolov(id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday id raqamli ma'lumot mavjud emas")
    db.query(Tolov).filter(Tolov.id == id).update({
        Tolov.status: False,
    })
    db.commit()
    return {"date": "Ma'lumot o'chirildi !"}
