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

from db.crud import *
from db.schemas.userSchema import *
from db.database import SessionLocal, engine
import db.model as model
from sqlalchemy.orm import Session
from sqlalchemy import select
model.Base.metadata.create_all(bind=engine)

def get_database_session():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

##daily 
# @app.task(daily.at("03:40"))
@app.task('every 60 seconds')
async def create_carpark(carpark: CarparkCreate, db: Session = get_database_session()):
    print('working')
    ura = URA()
    cp = ura.getCarparks()[0]
    r = Rate(
        weekdayMin=cp['weekdayMin'],
        endTime=cp['endTime'],
        weekdayRate=cp['weekdayRate'],
        startTime=cp['startTime'],
        sunPHRate=cp['sunPHRate'],
        sunPHMin=cp['sunPHMin'],
        satdayRate=cp['satdayRate'],
        satdayMin=cp['satdayMin']
    )
    l = Location(
        num=len(cp['geometries']),
        locations=[tuple(map(float, loc.split(','))) for loc in cp['geometries']]
    )
    carpark = Carpark(id=cp['ppCode'], name=cp['ppName'], locations=l, Rates=r)
    print(carpark)
    # return create_carpark(db=db, carpark=carpark)

@app.task('every 2 seconds')
async def do_task():
    print('test')
    '''test'''

if __name__ == "__main__":
    app.run()