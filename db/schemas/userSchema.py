from pydantic import BaseModel
from db.schemas.bookingSchema import Booking
from db.schemas.favouriteSchema import Favourite

class UserBase(BaseModel):
    username: str
    email: str
    bookings: list[Booking] = []
    favourites: list[Favourite] = []

class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    # is_active: bool # might not need

    class Config:
        orm_mode = True