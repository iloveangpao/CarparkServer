from datetime import time
from pydantic import BaseModel

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


class CarparkBase(BaseModel):
    id: int
    name: str
    locations: Location
    rates: Rate


class CarparkCreate(CarparkBase):
    pass


class Carpark(CarparkBase):
    id: int
    name: str
    locations: Location
    Rates: Rate

    class Config:
        orm_mode = True