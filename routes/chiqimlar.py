
from fastapi import APIRouter, Depends, HTTPException
from db import Base, engine,get_db

from sqlalchemy.orm import Session

from functions.chiqimlar import *
from routes.auth import get_current_active_user

Base.metadata.create_all(bind=engine)


from schemas.users import UserCurrent
from schemas.chiqimlar import *
router_chiqimlar = APIRouter()



@router_chiqimlar.post('/add', )
def add_chiqimlar(form: ChiqimlarCreate, db: Session = Depends(get_db),current_user: UserCurrent = Depends(get_current_active_user) ) : #
    if create_chiqimlar(form, current_user, db) :
        raise HTTPException(status_code = 200, detail = "Amaliyot muvaffaqiyatli amalga oshirildi")


@router_chiqimlar.get('/',  status_code = 200)
def get_chiqimlar(search: str = None, status: bool = True, id: int = 0,roll : str = None, page: int = 1, limit: int = 25, db: Session = Depends(get_db),current_user: UserCurrent = Depends(get_current_active_user) ) : # current_user: User = Depends(get_current_active_user)
    if id :
        return one_chiqimlar(id, db)
    else :
        return all_chiqimlar(search, status,roll, page, limit, db)




@router_chiqimlar.put("/update")
def chiqimlar_update(form: ChiqimlarUpdate, db: Session = Depends(get_db),current_user: UserCurrent = Depends(get_current_active_user)) :
    if update_chiqimlar(form,current_user, db) :
        raise HTTPException(status_code = 200, detail = "Amaliyot muvaffaqiyatli amalga oshirildi")




@router_chiqimlar.delete('/{id}',  status_code = 200)
def delete_xona(id: int = 0,db: Session = Depends(get_db), current_user: UserCurrent = Depends(get_current_active_user)) : # current_user: User = Depends(get_current_active_user)
    if id :
        return chiqimlar_delete(id,current_user, db)