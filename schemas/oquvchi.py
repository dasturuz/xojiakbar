from datetime import datetime

from pydantic import BaseModel



class OquvchiBase(BaseModel):
    ism:str
    familya: str
    yosh: int
    tel: int
    fan: str
    address: str
    soat: str

class OquvchiCreate(OquvchiBase):
    pass

class Oquvchiupdate(OquvchiBase):
    id:int
    user_id: int
    status:bool=True