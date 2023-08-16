
from fastapi import APIRouter, Depends, HTTPException
from db import Base, engine,get_db

from sqlalchemy.orm import Session

from functions.kurslar import *
from routes.auth import get_current_active_user

Base.metadata.create_all(bind=engine)


from schemas.users import UserCurrent
from schemas.kurslar import *
router_kurslar = APIRouter()



@router_kurslar.post('/add', )
def add_kurslar(form: KursCreate, db: Session = Depends(get_db),current_user: UserCurrent = Depends(get_current_active_user) ) : #
    if create_kurslar(form, current_user, db) :
        raise HTTPException(status_code = 200, detail = "Amaliyot muvaffaqiyatli amalga oshirildi")


@router_kurslar.get('/',  status_code = 200)
def get_kurslar(search: str = None, status: bool = True, id: int = 0,roll : str = None, page: int = 1, limit: int = 25, db: Session = Depends(get_db),current_user: UserCurrent = Depends(get_current_active_user) ) : # current_user: User = Depends(get_current_active_user)
    if id :
        return one_kurslar(id, db)
    else :
        return all_kurslar(search, status,roll, page, limit, db)




@router_kurslar.put("/update")
def kurslar_update(form: KursUpdate, db: Session = Depends(get_db),current_user: UserCurrent = Depends(get_current_active_user)) :
    if update_kurslar(form,current_user, db) :
        raise HTTPException(status_code = 200, detail = "Amaliyot muvaffaqiyatli amalga oshirildi")




@router_kurslar.delete('/{id}',  status_code = 200)
def delete_kurslar(id: int = 0,db: Session = Depends(get_db), current_user: UserCurrent = Depends(get_current_active_user)) : # current_user: User = Depends(get_current_active_user)
    if id :
        return kurslar_delete(id,current_user, db)