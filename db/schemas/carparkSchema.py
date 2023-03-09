from datetime import time
from pydantic import BaseModel

class Rate (BaseModel):
    weekdayMin: str = None
    endTime: time = None
    weekdayRate: float = None
    startTime: time = None
    sunPHRate: float = None
    sunPHMin: str = None
    satdayRate: float = None
    satdayMin: str = None

class location (BaseModel):
    num: int = None
    locations = tuple = None

class Carpark(BaseModel):
    id = int
    name = str
    location = location
    Rates = Rate

    class Config:
        orm_mode = True