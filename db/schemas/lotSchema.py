from pydantic import BaseModel


class LotBase(BaseModel):
    pass


class LotCreate(LotBase):
    pass


class Lot(LotBase):
    id: int
    carpark_id: int
    class Config:
        orm_mode = True