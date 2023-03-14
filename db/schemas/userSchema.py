from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    username : str = None
    class Config:
        orm_mode = True

class UserInDB(User):
    hashed_password : str

class Token(BaseModel):
    access_token : str
    token_type : str

class TokenData(BaseModel):
    username : Optional[str] = None
