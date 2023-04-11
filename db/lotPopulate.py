import sys
sys.path.append('/code/')
from crud import *
from schemas import carparkSchema
from database import SessionLocal
from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.lotSchema import *

def get_database_session():
    try:
        db = SessionLocal()
        return db
    finally:
        db.close()

db = get_database_session()
cp: list[carparkSchema.Carpark] = get_carparks(db)
db.close()
for carpark in cp:
    avail = carpark.Availability
    print('code =', carpark.cp_code)
    print(avail)
    if not avail:
        avail = 0

    for i in range(6):
        lot = LotCreate()
        avail += 1
        db = get_database_session()
        create_lot(db, lot, carpark.cp_code, False)
        db.close()

    db = get_database_session()
    update_carpark(db, 'cp_code', carpark.cp_code, 'Availability', avail)
    db.close()

