# Create Rocketry app
import asyncio
from rocketry import Rocketry
from rocketry.conds import every, daily
app = Rocketry(execution="async")


# Create some tasks

# @app.task('every 5 seconds')
# async def do_things():
#     print('hello')
#     "This runs for short time"
#     await asyncio.sleep(1)

from app.ura import URA

import db.crud as crud
from db.schemas.carparkSchema import *
from db.database import SessionLocal, engine
import db.model as model
from sqlalchemy.orm import Session
from sqlalchemy import select
import json

model.Base.metadata.create_all(bind=engine)

def get_database_session():
    try:
        db = SessionLocal()
        return db
    finally:
        db.close()

# ##daily 
# # @app.task(daily.at("03:40"))
@app.task('every 15 seconds')
async def syncCarparkAvail():
    avails = URA().getAvail()

    for cp in avails:
        db = get_database_session()
        crud.update_carpark(db, 'cp_code', cp['carparkNo'], 'Availability', cp['lotsAvailable'])
        db.close()

@app.task('every 15 minutes')
async def add_all_carparks():
    print('working')
    try:
        cp = URA().handleExtraRates(URA().datingCP(URA().getCPFinal()))
        db = get_database_session()
        crud.del_all_carparks(db)
        db.close()
        db = get_database_session()
        crud.create_carpark(db,cp)
        db.close()
    except Exception as e:
        print(e)
    
    print('done')






if __name__ == "__main__":
    app.run()