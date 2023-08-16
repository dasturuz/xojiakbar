from datetime import datetime

from pydantic import BaseModel


class KursBase(BaseModel):
    oqtuvchi_id: int
    fan_id: int
    xona: int
    kurs_muddati: int
    soat: str


class KursCreate(KursBase):
    pass


class KursUpdate(KursBase):
    id: int
    user_id: int
    status: bool = True
