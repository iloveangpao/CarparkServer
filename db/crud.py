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
from db.schemas.lotSchema import *
from db.schemas.bookingSchema import *
from db.schemas.favouriteSchema import *
import importlib



# CARPARKS
def object_as_dict(obj):
    return {c.key: getattr(obj, c.key)
            for c in inspect(obj).mapper.column_attrs}

def get_carparks(db: Session, skip: int = 0, limit: int = -1):
    # print(db.query(model.Carparks).offset(skip).limit(limit).all())
    if limit > 0:
        query = db.query(model.Carparks).offset(skip).limit(limit).all()
    else:
        query = db.query(model.Carparks).offset(skip).all()
    
    carparkList = []
    for i in query:
        carparkList.append(Carpark(cp_code = i.cp_code, name = i.name, locations = i.locations, Availability = i.Availability, rate = i.rate, min = i.min, lots = i.lots))
    
    return carparkList

def get_carpark_by_code(db: Session, cp_code: str):
    return db.query(model.Carparks).filter(model.Carparks.cp_code == cp_code).first()

def update_carpark(db: Session, filter: str, filterVal, toUpdate: str, newVal):
    db.query(model.Carparks).\
       filter(getattr(model.Carparks, filter) == filterVal).\
       update({toUpdate : newVal})
    db.commit()

def get_carparks_basic_info(db: Session):
    return db.query(model.Carparks).add_column(Carpark.id).add_column(Carpark.name).all()


def create_carpark(db: Session, cp: dict):
    for carparkData in cp:
        if carparkData['vehCat'] == "Car":
            try:
                num = len(carparkData['geometries'])
                locations = []
                for loc in carparkData['geometries']:
                    locations.append(tuple(loc['coordinates'].split(',')))
                l = Location(
                    num = num,
                    locations = locations
                )
                carpark = Carpark(id=0,cp_code = carparkData['ppCode'], name=carparkData['ppName'], locations=l, rate=carparkData['rate'], min = carparkData['min'])
                db_carpark = model.Carparks(name=carpark.name, cp_code = carpark.cp_code,
                                locations=carpark.locations.dict(), rate=carpark.rate, min = carpark.min)
                db.add(db_carpark)
                db.commit()
                db.refresh(db_carpark)
            except Exception as e:
                print(e)

def del_all_carparks(db: Session):
    deleted = db.query(model.Carparks).delete()
    db.commit()
    print(str(deleted) + " rows were deleted")
# USERS
def get_user(db: Session, user_id: int):
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


# LOTS
def create_lot(db: Session, lot: LotCreate, cp_code: str):
    db_lot = model.Lot(**lot.dict(), cp_code=cp_code)
    db.add(db_lot)
    db.commit()
    db.refresh(db_lot)
    return db_lot


def get_lots(db: Session, skip: int = 0, limit: int = -1):
    if limit > 0:
        query = db.query(model.Carparks).offset(skip).limit(limit).all()
    else:
        query = db.query(model.Carparks).offset(skip).all()

    return query

def get_lot_by_attr(db: Session, attribute : str, searchVal):
    return db.query(model.Lot).filter(getattr(model.Lot,attribute) == searchVal).first()




# BOOKINGS
def create_booking(db: Session, booking: BookingCreate, user_id: int, lot_id: int):
    db_booking = model.Booking(**booking.dict(), user_id=user_id, lot_id=lot_id)
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking


def get_bookings(db: Session, skip: int = 0, limit: int = 100):
    return db.query(model.Booking).offset(skip).limit(limit).all()

def get_booking_by_attr(db: Session, attribute : str, searchVal):
    return db.query(model.Booking).filter(getattr(model.Booking,attribute) == searchVal).first()


# FAVOURITES
def create_favourite(db: Session, favourite: FavouriteCreate, user_id, carpark_id):
    db_favourite = model.Favourite(**favourite.dict(), user_id=user_id, carpark_id=carpark_id)
    db.add(db_favourite)
    db.commit()
    db.refresh(db_favourite)
    return db_favourite


def get_favourites(db: Session, skip: int = 0, limit: int = 100):
    return db.query(model.Favourite).offset(skip).limit(limit).all()

def get_favourites_by_attr(db: Session, attribute : str, searchVal):
    return db.query(model.Favourite).filter(getattr(model.Favourite,attribute) == searchVal).first()