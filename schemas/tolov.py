from pydantic import BaseModel


class TolovBase(BaseModel):
    oquvchi_id: int
    fan_id: int
    oy: str
    narx: int
    turi: str


class TolovCreate(TolovBase):
    pass


class TolovUpdate(TolovBase):
    id: int
    status: bool = True
    user_id:int