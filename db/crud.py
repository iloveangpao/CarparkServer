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
    print(db.query(Carparks).offset(skip).limit(limit).all())
    return db.query(Carparks).offset(skip).limit(limit).all()

def get_carparks_basic_info(db: Session):
    return db.query(Carparks).add_column(Carpark.id).add_column(Carpark.name).all()

def create_carpark(db: Session, carpark: Carpark):
    print(carpark.locations)
    db_carpark = Carparks(name=carpark.name, cp_code = carpark.cp_code,
                                locations=carpark.locations.dict(), Rates=carpark.Rates.dict())
    db.add(db_carpark)
    db.commit()
    db.refresh(db_carpark)
    return db_carpark