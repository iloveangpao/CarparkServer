'''
This file contains essential CRUD functions.
- CREATE
- READ
- UPDATE
- DELETE
The functions can be reused elsewhere
'''


from sqlalchemy.orm import Session

from db import model
from db.schemas.carparkSchema import *
from db.schemas.userSchema import *

# CARPARKS
def get_carparks(db: Session, skip: int = 0, limit: int = 100):
    print(db.query(model.Carparks).offset(skip).limit(limit).all())
    return db.query(model.Carparks).offset(skip).limit(limit).all()


def get_carparks_basic_info(db: Session):
    return db.query(model.Carparks).add_column(Carpark.id).add_column(Carpark.name).all()


def create_carpark(db: Session, carpark: Carpark):
    # print(carpark.locations)
    try:
        db_carpark = model.Carparks(name=carpark.name, cp_code = carpark.cp_code,
                                locations=carpark.locations.dict(), Rates=carpark.Rates.dict())
        db.add(db_carpark)
        db.commit()
        db.refresh(db_carpark)
    except Exception as e:
        print(e)


# USERS
def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()


def create_user(db: Session, user: UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = model.User(name=user.name, email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
    