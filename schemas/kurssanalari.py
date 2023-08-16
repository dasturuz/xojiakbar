from datetime import datetime

from pydantic import BaseModel



class KurssananalrBase(BaseModel):
    bor:str
    yoq: str
    oqtuvchi_id : int
    fan_id: int
    xona_id: int
    boshi: str
    oxiri: str
    oquvchi_id: int
    kurs_muddati: int
    soat: str

class KurssananalrCreate(KurssananalrBase):
    pass

class KurssananalrUpdate(KurssananalrBase):
    id:int
    user_id: int
    status:bool=True