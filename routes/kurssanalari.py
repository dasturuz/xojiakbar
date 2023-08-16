
from fastapi import APIRouter, Depends, HTTPException
from db import Base, engine,get_db

from sqlalchemy.orm import Session

from functions.kurssanalari import *
from routes.auth import get_current_active_user

Base.metadata.create_all(bind=engine)


from schemas.users import UserCurrent
from schemas.kurssanalari import *
router_kurssanalari = APIRouter()



@router_kurssanalari.post('/add', )
def add_kurssanalari(form: KurssananalrCreate, db: Session = Depends(get_db),current_user: UserCurrent = Depends(get_current_active_user) ) : #
    if create_kurssanalari(form, current_user, db) :
        raise HTTPException(status_code = 200, detail = "Amaliyot muvaffaqiyatli amalga oshirildi")


@router_kurssanalari.get('/',  status_code = 200)
def get_kurssanalari(search: str = None, status: bool = True, id: int = 0,roll : str = None, page: int = 1, limit: int = 25, db: Session = Depends(get_db),current_user: UserCurrent = Depends(get_current_active_user) ) : # current_user: User = Depends(get_current_active_user)
    if id :
        return one_kurssanalari(id, db)
    else :
        return all_kurssanalari(search, status,roll, page, limit, db)




@router_kurssanalari.put("/update")
def kurssanalari_update(form: KurssananalrUpdate, db: Session = Depends(get_db),current_user: UserCurrent = Depends(get_current_active_user)) :
    if update_kurssanalari(form,current_user, db) :
        raise HTTPException(status_code = 200, detail = "Amaliyot muvaffaqiyatli amalga oshirildi")




@router_kurssanalari.delete('/{id}',  status_code = 200)
def delete_kurssanalari(id: int = 0,db: Session = Depends(get_db), current_user: UserCurrent = Depends(get_current_active_user)) : # current_user: User = Depends(get_current_active_user)
    if id :
        return kurssanalari_delete(id,current_user, db)