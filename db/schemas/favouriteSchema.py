from pydantic import BaseModel


class FavouriteBase(BaseModel):
    pass


class FavouriteCreate(FavouriteBase):
    pass


class Favourite(FavouriteBase):
    id: int
    user_id: int
    cp_code: str
    class Config:
        orm_mode = True