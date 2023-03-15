'''
This file contains essential CRUD functions.
- CREATE
- READ
- UPDATE
- DELETE
The functions can be reused elsewhere
'''


from sqlalchemy.orm import Session

from db.model import *
from db.schemas.carparkSchema import *


def get_carparks(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Carparks).offset(skip).limit(limit).all()

def get_carparks_basic_info(db: Session):
    return db.query(Carparks).add_column(Carpark.id).add_column(Carpark.name).all()

def create_carpark(db: Session, carpark: CarparkCreate):
    db_carpark = Carpark(id=carpark.id, name=carpark.name,
                                locations=carpark.locations, rates=carpark.rates)
    db.add(db_carpark)
    db.commit()
    db.refresh(db_carpark)
    return db_carpark