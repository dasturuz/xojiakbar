from pydantic import BaseModel


class FanlarBase(BaseModel):
    nomi: str
    user_id: int


class FanlarCreate(FanlarBase):
    pass


class FanlarUpdate(FanlarBase):
    id: int
    user_id: int
    status: bool = True
