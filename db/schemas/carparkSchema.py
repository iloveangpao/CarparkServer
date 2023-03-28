from datetime import time
from pydantic import BaseModel
from typing import Optional
from db.schemas.lotSchema import Lot

class Rate(BaseModel):
    weekdayMin: str
    endTime: time
    weekdayRate: float
    startTime: time
    sunPHRate: float
    sunPHMin: str
    satdayRate: float
    satdayMin: str


class Location(BaseModel):
    num: int = None
    locations: list[tuple] = None


'''class CarparkBase(BaseModel):
    id: str
    name: str
    locations: Location
    Rates: Rate


class CarparkCreate(CarparkBase):
    pass
'''


class Carpark(BaseModel):
    id: int
    cp_code : str
    name: str
    locations: Location
    Rates: Rate
    # BookableSlots: Optional[dict] = None
    Availability: Optional[int] = None
    lots: list[Lot] = []

    class Config:
        orm_mode = True