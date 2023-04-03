import sys
sys.path.append('/code/')
from crud import *
from database import SessionLocal, engine
import model as model
from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.lotSchema import *

model.Base.metadata.create_all(bind=engine)

def get_database_session():
    try:
        db = SessionLocal()
        return db
    finally:
        db.close()

db = get_database_session()
cp = get_carparks(db)

for carpark in cp:
    create_lot(db, LotCreate, carpark['cp_code'])

db.close()