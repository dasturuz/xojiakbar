
from fastapi import APIRouter, Depends, HTTPException
from db import Base, engine,get_db

from sqlalchemy.orm import Session

from functions.xona import *
from routes.auth import get_current_active_user

Base.metadata.create_all(bind=engine)


from schemas.users import UserCurrent
from schemas.xona import *
router_xona = APIRouter()



@router_xona.post('/add', )
def add_xona(form: XonaCreate, db: Session = Depends(get_db),current_user: UserCurrent = Depends(get_current_active_user) ) : #
    if create_xona(form, current_user, db) :
        raise HTTPException(status_code = 200, detail = "Amaliyot muvaffaqiyatli amalga oshirildi")


@router_xona.get('/',  status_code = 200)
def get_xona(search: str = None, status: bool = True, id: int = 0,roll : str = None, page: int = 1, limit: int = 25, db: Session = Depends(get_db),current_user: UserCurrent = Depends(get_current_active_user) ) : # current_user: User = Depends(get_current_active_user)
    if id :
        return one_xona(id, db)
    else :
        return all_xona(search, status,roll, page, limit, db)




@router_xona.put("/update")
def xona_update(form: XonaUpdate, db: Session = Depends(get_db),current_user: UserCurrent = Depends(get_current_active_user)) :
    if update_xona(form,current_user, db) :
        raise HTTPException(status_code = 200, detail = "Amaliyot muvaffaqiyatli amalga oshirildi")




@router_xona.delete('/{id}',  status_code = 200)
def delete_xona(id: int = 0,db: Session = Depends(get_db), current_user: UserCurrent = Depends(get_current_active_user)) : # current_user: User = Depends(get_current_active_user)
    if id :
        return xona_delete(id,current_user, db)