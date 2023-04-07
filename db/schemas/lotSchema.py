from pydantic import BaseModel


class LotBase(BaseModel):
    pass


class LotCreate(LotBase):
    pass


class Lot(LotBase):
    id: int
    cp_code: str
    occupied: bool
    class Config:
        orm_mode = True