from pydantic import BaseModel
from datetime import datetime


class BookingBase(BaseModel):
    start_time: str # or SQLAlchemy DateTime
    

class BookingCreate(BookingBase):
    pass


class Booking(BookingBase):
    id: int
    user_id: int
    lot_id: int
    class Config:
        orm_mode = True