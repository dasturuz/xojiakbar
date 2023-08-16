from pydantic import BaseModel



class ChiqimlarBase(BaseModel):
    oqtuvchi_id : int
    pul: int
    turi: str
    comment: str


class ChiqimlarCreate(ChiqimlarBase):
    pass

class ChiqimlarUpdate(ChiqimlarBase):
    id:int
    user_id: int
    status:bool=True