from pydantic import BaseModel



class XonaBase(BaseModel):
    xona_nomi:str
    raqami: int



class XonaCreate(XonaBase):
    pass

class XonaUpdate(XonaBase):
    id:int
    user_id: int
    status:bool=True