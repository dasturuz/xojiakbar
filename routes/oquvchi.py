
from fastapi import APIRouter, Depends, HTTPException
from db import Base, engine,get_db

from sqlalchemy.orm import Session

from functions.oquvchi import *
from routes.auth import get_current_active_user

Base.metadata.create_all(bind=engine)


from schemas.users import UserCurrent
from schemas.oquvchi import *
router_oquvchi = APIRouter()



@router_oquvchi.post('/add', )
def add_oquvchi(form: OquvchiCreate, db: Session = Depends(get_db),current_user: UserCurrent = Depends(get_current_active_user) ) : #
    if create_oquvchi(form, current_user, db) :
        raise HTTPException(status_code = 200, detail = "Amaliyot muvaffaqiyatli amalga oshirildi")


@router_oquvchi.get('/',  status_code = 200)
def get_oquvchi(search: str = None, status: bool = True, id: int = 0,roll : str = None, page: int = 1, limit: int = 25, db: Session = Depends(get_db),current_user: UserCurrent = Depends(get_current_active_user) ) : # current_user: User = Depends(get_current_active_user)
    if id :
        return one_oquvchi(id, db)
    else :
        return all_oquvchi(search, status,roll, page, limit, db)




@router_oquvchi.put("/update")
def oquvchi_update(form: Oquvchiupdate, db: Session = Depends(get_db),current_user: UserCurrent = Depends(get_current_active_user)) :
    if update_oquvchi(form,current_user, db) :
        raise HTTPException(status_code = 200, detail = "Amaliyot muvaffaqiyatli amalga oshirildi")




@router_oquvchi.delete('/{id}',  status_code = 200)
def delete_oquvchi(id: int = 0,db: Session = Depends(get_db), current_user: UserCurrent = Depends(get_current_active_user)) : # current_user: User = Depends(get_current_active_user)
    if id :
        return oquvchi_delete(id,current_user, db)