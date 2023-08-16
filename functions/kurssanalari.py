from passlib.context import CryptContext


pwd_context = CryptContext(schemes=['bcrypt'])

from fastapi import HTTPException
from models.kurssanalari import Kurssanalri

from utils.pagination import pagination


def all_kurssanalari(search, status, roll, page, limit, db):
    if search:
        search_formatted = "%{}%".format(search)
        search_filter = Kurssanalri.oqtuvchi_id.like(search_formatted) | Kurssanalri.fan_id.like(search_formatted)| Kurssanalri.oquvchi_id.like(search_formatted)
    else:
        search_filter = Kurssanalri.id > 0
    if status in [True, False]:
        status_filter = Kurssanalri.status == status
    else:
        status_filter = Kurssanalri.id > 0

    if roll:
        roll_filter = Kurssanalri.fan_id == roll
    else:
        roll_filter = Kurssanalri.id > 0

    users = db.query(Kurssanalri).filter(search_filter, status_filter, roll_filter).order_by(Kurssanalri.bor.asc())
    if page and limit:
        return pagination(users, page, limit)
    else:
        return users.all()


def one_kurssanalari(id, db):
    return db.query(Kurssanalri).filter(Kurssanalri.id == id).first()


def kurssanalari_current(user, db):
    return db.query(Kurssanalri).filter(Kurssanalri.id == user.id).first()


def create_kurssanalari(form, user, db):
    user_verification = db.query(Kurssanalri).filter(Kurssanalri.oquvchi_id == form.oquvchi_id).first()
    if user_verification:
        raise HTTPException(status_code=400, detail="Bunday oquvchi_id mavjud")
    number_verification = db.query(Kurssanalri).filter(Kurssanalri.fan_id == form.fan_id).first()
    if number_verification:
        raise HTTPException(status_code=400, detail="Bunday fan_id mavjud")

    new_user_db = Kurssanalri(
        bor=form.bor,
        yoq=form.yoq,
        oqtuvchi_id=form.oqtuvchi_id,
        fan_id=form.fan_id,
        xona_id=form.xona_id,
        boshi=form.boshi,
        oxiri=form.oxiri,
        oquvchi_id=form.oquvchi_id,
        kurs_muddati=form.kurs_muddati,
        soat=form.soat,
        user_id=user.id

    )
    db.add(new_user_db)
    db.commit()
    db.refresh(new_user_db)

    return new_user_db


def update_kurssanalari(form, user, db):
    if one_kurssanalari(form.id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday id raqamli foydalanuvchi mavjud emas")
    user_verification = db.query(Kurssanalri).filter(Kurssanalri.oqtuvchi_id == form.oqtuvchi_id).first()
    if user_verification and user_verification.id != form.id:
        raise HTTPException(status_code=400, detail="Bunday oqtuvchi_id mavjud")

    db.query(Kurssanalri).filter(Kurssanalri.id == form.id).update({
        Kurssanalri.id: form.id,
        Kurssanalri.bor: form.bor,
        Kurssanalri.yoq: form.yoq,
        Kurssanalri.oqtuvchi_id: form.oqtuvchi_id,
        Kurssanalri.fan_id: form.fan_id,
        Kurssanalri.xona_id: form.xona_id,
        Kurssanalri.boshi: form.boshi,
        Kurssanalri.oxiri: form.oxiri,
        Kurssanalri.oquvchi_id: form.oquvchi_id,
        Kurssanalri.kurs_muddati: form.kurs_muddati,
        Kurssanalri.status: form.status,
        Kurssanalri.user_id: form.user_id

    })
    db.commit()

    return one_kurssanalari(form.id, db)


def update_kurssanalari_salary(id, salary, db):
    if one_kurssanalari(id, db) is None:
        raise HTTPException(status_code=400, detail=f"Bunday {id} raqamli hodim mavjud emas")

    db.query(Kurssanalri).filter(Kurssanalri.id == id).update({
        Kurssanalri.salary: salary,

    })
    db.commit()
    return one_kurssanalari(id, db)


def kurssanalari_delete(id, user, db):
    if one_kurssanalari(id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday id raqamli ma'lumot mavjud emas")
    db.query(Kurssanalri).filter(Kurssanalri.id == id).update({
        Kurssanalri.status: False,
    })
    db.commit()
    return {"date": "Ma'lumot o'chirildi !"}
