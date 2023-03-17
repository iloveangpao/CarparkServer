from pydantic import BaseModel
from typing import Optional

'''class User(BaseModel):
    username : str = None
    class Config:
        orm_mode = True

class UserInDB(User):
    hashed_password : str

class Token(BaseModel):
    access_token : str
    token_type : str

class TokenData(BaseModel):
    username : Optional[str] = None'''


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    username: str
    # is_active: bool # might not need
    # bookings: List[Booking] = [] # later add with bookings

    class Config:
        orm_mode = True