
from fastapi import APIRouter, Depends, HTTPException
from db import Base, engine,get_db

from sqlalchemy.orm import Session

from routes.auth import get_current_active_user

Base.metadata.create_all(bind=engine)


from functions.oqtuvchi import *
from schemas.users import UserCurrent
from schemas.oqtuvchi import *
router_oqtuvchi = APIRouter()



@router_oqtuvchi.post('/add', )
def add_oqtuvchi(form: OqtuvchiCreate, db: Session = Depends(get_db),current_user: UserCurrent = Depends(get_current_active_user) ) : #
    if create_oqtuvchi(form, current_user, db) :
        raise HTTPException(status_code = 200, detail = "Amaliyot muvaffaqiyatli amalga oshirildi")


@router_oqtuvchi.get('/',  status_code = 200)
def get_oqtuvchi(search: str = None, status: bool = True, id: int = 0,roll : str = None, page: int = 1, limit: int = 25, db: Session = Depends(get_db),current_user: UserCurrent = Depends(get_current_active_user) ) : # current_user: User = Depends(get_current_active_user)
    if id :
        return one_oqtuvchi(id, db)
    else :
        return all_oqtuvchi(search, status,roll, page, limit, db)




@router_oqtuvchi.put("/update")
def oqtuvchi_update(form: Oqtuvchiupdate, db: Session = Depends(get_db),current_user: UserCurrent = Depends(get_current_active_user)) :
    if update_oqtuvchi(form,current_user, db) :
        raise HTTPException(status_code = 200, detail = "Amaliyot muvaffaqiyatli amalga oshirildi")




@router_oqtuvchi.delete('/{id}',  status_code = 200)
def delete_oqtuvchi(id: int = 0,db: Session = Depends(get_db), current_user: UserCurrent = Depends(get_current_active_user)) : # current_user: User = Depends(get_current_active_user)
    if id :
        return oqtuvchi_delete(id,current_user, db)