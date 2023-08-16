from datetime import datetime
from typing import Optional

from pydantic import BaseModel



class OqtuvchiBase(BaseModel):
    ism:str
    familya: str
    tel: int
    fan_id: int
    password: str
    roll:str
    username:str


class OqtuvchiCreate(OqtuvchiBase):
    pass

class Oqtuvchiupdate(OqtuvchiBase):
    id:int
    user_id: int
    status:bool=True

