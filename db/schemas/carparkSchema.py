from datetime import time
from pydantic import BaseModel
from typing import Optional
from db.schemas.lotSchema import Lot

class Rate(BaseModel):
    weekdayMin: str
    endTime: str #time
    weekdayRate: str #float
    startTime: str #time
    sunPHRate: str #float
    sunPHMin: str
    satdayRate: str #float
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
    lots: list[Lot] = []

    class Config:
        orm_mode = True