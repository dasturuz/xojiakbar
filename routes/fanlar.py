
from fastapi import APIRouter, Depends, HTTPException
from db import Base, engine,get_db

from sqlalchemy.orm import Session

from functions.fanlar import *
from routes.auth import get_current_active_user

Base.metadata.create_all(bind=engine)


from schemas.users import UserCurrent
from schemas.fanlar import *
router_fanlar = APIRouter()



@router_fanlar.post('/add', )
def add_fanlar(form: FanlarCreate, db: Session = Depends(get_db),current_user: UserCurrent = Depends(get_current_active_user) ) : #
    if create_fanlar(form, current_user, db) :
        raise HTTPException(status_code = 200, detail = "Amaliyot muvaffaqiyatli amalga oshirildi")


@router_fanlar.get('/',  status_code = 200)
def get_fanlar(search: str = None, status: bool = True, id: int = 0,roll : str = None, page: int = 1, limit: int = 25, db: Session = Depends(get_db),current_user: UserCurrent = Depends(get_current_active_user) ) : # current_user: User = Depends(get_current_active_user)
    if id :
        return one_fanlar(id, db)
    else :
        return all_fanlar(search, status,roll, page, limit, db)




@router_fanlar.put("/update")
def fanlar_update(form: FanlarUpdate, db: Session = Depends(get_db),current_user: UserCurrent = Depends(get_current_active_user)) :
    if update_fanlar(form,current_user, db) :
        raise HTTPException(status_code = 200, detail = "Amaliyot muvaffaqiyatli amalga oshirildi")




@router_fanlar.delete('/{id}',  status_code = 200)
def delete_xona(id: int = 0,db: Session = Depends(get_db), current_user: UserCurrent = Depends(get_current_active_user)) : # current_user: User = Depends(get_current_active_user)
    if id :
        return fanlar_delete(id,current_user, db)