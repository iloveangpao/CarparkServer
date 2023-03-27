'''
This file contains essential CRUD functions.
- CREATE
- READ
- UPDATE
- DELETE
The functions can be reused elsewhere
'''


from sqlalchemy.orm import Session
from sqlalchemy import inspect

from db import model
from db.schemas.carparkSchema import *
from db.schemas.userSchema import *

# CARPARKS
def object_as_dict(obj):
    return {c.key: getattr(obj, c.key)
            for c in inspect(obj).mapper.column_attrs}

def get_carparks(db: Session, skip: int = 0, limit: int = -1):
    # print(db.query(model.Carparks).offset(skip).limit(limit).all())
    if limit > 0:
        cp = db.query(model.Carparks).offset(skip).limit(limit).all()
    else:
        cp = db.query(model.Carparks).offset(skip).all()
    cpsAsDict = []
    for temp in cp:
        cpsAsDict.append(object_as_dict(temp))
    return cpsAsDict

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
def get_user(db: Session, user_id: str):
    return db.query(model.User).filter(model.User.id == user_id).first()


def get_user_by_username(db: Session, username: str):
    return db.query(model.User).filter(model.User.username == username).first()


def get_user_by_email(db: Session, email: str):
    return db.query(model.User).filter(model.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(model.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: UserCreate, hashed_password):
    db_user = model.User(username=user.username, email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user





    