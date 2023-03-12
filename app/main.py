class Unbuffered(object):
   def __init__(self, stream):
       self.stream = stream
   def write(self, data):
       self.stream.write(data)
       self.stream.flush()
   def writelines(self, datas):
       self.stream.writelines(datas)
       self.stream.flush()
   def __getattr__(self, attr):
       return getattr(self.stream, attr)

import sys
sys.stdout = Unbuffered(sys.stdout)


from typing import Union
from fastapi import FastAPI, Depends
import json

#class for accessing URA api
from app.ura import URA

import os
print(os.getcwd())

# db stuff
# import db.schemas.carparkSchema as carparkSchema
from db.database import SessionLocal, engine
import db.model as model
from sqlalchemy.orm import Session
model.Base.metadata.create_all(bind=engine)

def get_database_session():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

def create_carpark(db: Session = Depends(get_database_session), carparkData : json = None):
    
    carpark = model.Carparks()
    db.add(carpark)
    db.commit()

uraGetter = URA()
getter = uraGetter.getCarparks
result = getter()
print(result)
###making endpoints
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

# @app.get("/carparkInfo/{requirement}")

# async def carpark(requirement):
#     uraGetter = URA()
#     getter = getattr(uraGetter, requirement)
#     result = getter()
#     return {requirement : result}

# @app.get("/items/{item_id}")

# def read_item(item_id : int , q: Union[str,None] = None):
#     return {"item_id": item_id, "q": q}

# @app.get("/carparkInfo")
# async def read_movies(db: Session = Depends(get_database_session)):
#     records = db.query(Carparks).all()
#     return records




###daily scheduler
# from rocketry import Rocketry
# from rocketry.conds import every, after_success

# # Creating the Rocketry app
# app = Rocketry(config={"task_execution": "async"})

# # Creating some tasks
# @app.task('daily')
# async def getURAToken():
#     uraGetter = URA()
#     getter = uraGetter.getToken
#     result = getter()
#     return {result}

# @app.task(after_success(getURAToken))
# async def getCarparks():
#     uraGetter = URA()
#     getter = uraGetter.getCarparks
#     result = getter()
#     return result