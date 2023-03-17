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
model.Base.metadata.create_all(bind=engine)

def get_database_session():
    try:
        db = SessionLocal()
        return db
    finally:
        db.close()

##daily 
# @app.task(daily.at("03:40"))
@app.task('every 60 seconds')
async def create_carpark():
    print('working')
    ura = URA()
    cp = ura.getCarparks()
    temp = cp[0]
    r = Rate(
        weekdayMin=temp['weekdayMin'],
        endTime=temp['endTime'],
        weekdayRate=temp['weekdayRate'],
        startTime=temp['startTime'],
        sunPHRate=temp['sunPHRate'],
        sunPHMin=temp['sunPHMin'],
        satdayRate=temp['satdayRate'],
        satdayMin=temp['satdayMin']
    )
    print('aftrate')
    
    print(temp)
    print(type(temp['geometries']))
    print(temp['geometries'])
    num = len(temp['geometries'])
    print(num)
    locations = []
    for loc in temp['geometries']:
        print(loc)
        locations.append(tuple(loc['coordinates'].split(',')))
    print(locations)
    l = Location(
        num = num,
        locations = locations
    )
    print('b4parsing')
    # print(cp)
    carpark = Carpark(id=0,cp_code = temp['ppCode'], name=temp['ppName'], locations=l, Rates=r)
    print('yay',carpark)
    try:
        db = get_database_session()
        crud.create_carpark(db=db, carpark=carpark)
        db.close()
    except Exception as e:
        print(e)
    print('hehe')

# @app.task('every 2 seconds')
# async def do_task():
#     await print('test')

if __name__ == "__main__":
    app.run()