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
@app.task('daily')
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

@app.task("after task 'create_carpark'")
async def add_all_carparks():
    print('working')
    ura = URA()
    cp = ura.getCarparks()
    db = get_database_session()
    db.query(model.Carparks).delete()
    for carpark in cp:
        r = Rate(
            weekdayMin=carpark['weekdayMin'],
            endTime=carpark['endTime'],
            weekdayRate=carpark['weekdayRate'],
            startTime=carpark['startTime'],
            sunPHRate=carpark['sunPHRate'],
            sunPHMin=carpark['sunPHMin'],
            satdayRate=carpark['satdayRate'],
            satdayMin=carpark['satdayMin']
        )
        
        num = len(carpark['geometries'])
        locations = []
        for loc in carpark['geometries']:
            locations.append(tuple(loc['coordinates'].split(',')))
        l = Location(
            num = num,
            locations = locations
        )
        carpark = Carpark(id=0,cp_code = carpark['ppCode'], name=carpark['ppName'], locations=l, Rates=r)

        try:
            crud.create_carpark(db=db, carpark=carpark)
            db.close()
        except Exception as e:
            print(e)

if __name__ == "__main__":
    app.run()