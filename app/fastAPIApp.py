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

from fastapi import Depends, FastAPI, HTTPException, status, Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
import json
from contextlib import asynccontextmanager
from datetime import datetime, timedelta, timezone
import os
from typing import Optional, Annotated
print(os.listdir())
import db.schemas.userSchema as userSchema
from db.database import SessionLocal, engine
import db.model as model
from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from app.ura import URA
from app.onemap import OneMap
from db.schemas.carparkSchema import *
import db.crud as crud
import os, json
from filter import Filter

model.Base.metadata.create_all(bind=engine)

def get_database_session():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

@asynccontextmanager
async def lifespan(app: FastAPI):
    masterList = URA().handleExtraRates(URA().datingCP(URA().getCPFinal()))
    db = get_database_session()
    dbList = crud.get_carparks(db)
    db.close()
    cpCodeList = []
    for i in dbList:
        cpCodeList.append(i.cp_code)
    toInsert = []
    for j in masterList:
        print(j)
        if j['ppCode'] in cpCodeList:
            toInsert.append(j)
    db = get_database_session()
    crud.create_carpark(db,toInsert)
    db.close()
    yield

app = FastAPI(lifespan = lifespan)

@app.on_event("startup")
async def startup_event():
    print('in')
    masterList = URA().handleExtraRates(URA().datingCP(URA().getCPFinal()))
    db = get_database_session()
    dbList = crud.get_carparks(db)
    db.close()
    cpCodeList = []
    for i in dbList:
        cpCodeList.append(i.cp_code)
    toInsert = []
    for j in masterList:
        print(j)
        if j['ppCode'] not in cpCodeList:
            toInsert.append(j)
    db = get_database_session()
    crud.create_carpark(db,toInsert)
    db.close()
    yield


@app.get("/")
async def root():
    return {"message": "Hello World"}

###Authentication
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


'''async was giving some errors. seems like it works without async, but leaving the commented line here first'''
#async def get_user(db: AsyncSession, username: str) -> model.User:
def get_user(db: AsyncSession, username: str) -> model.User:
    #result = await db.execute(select(model.User).filter_by(username=username))
    result = db.execute(select(model.User).filter_by(username=username))
    return result.scalars().first()


'''async was giving some errors. seems like it works without async, but leaving the commented line here first'''
#async def authenticate_user(db: AsyncSession, username: str, password: str) -> model.User:
def authenticate_user(db: AsyncSession, username: str, password: str) -> model.User:
    #user = await get_user(db, username)
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


'''async was giving some errors. seems like it works without async, but leaving the commented line here first'''
#async def get_current_user(db: AsyncSession = Depends(get_database_session), token: str = Depends(oauth2_scheme)) -> model.User:
def get_current_user(db: AsyncSession = Depends(get_database_session), token: str = Depends(oauth2_scheme)) -> model.User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


'''dont know if we need the disabled feature or not. this fn was causing me errors, but if we dn then screw it'''
# async def get_current_active_user(current_user: model.User = Depends(get_current_user)):
#     if current_user.disabled:
#         raise HTTPException(status_code=400, detail="Inactive user")
#     return current_user


@app.post("/token", response_model=Token)
async def login_for_access_token(db: AsyncSession = Depends(get_database_session), form_data: OAuth2PasswordRequestForm = Depends()):
    #user = await authenticate_user(db, form_data.username, form_data.password)
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


'''basic functions for reading/creating users'''

@app.get("/users/me/", response_model=userSchema.User)
async def read_users_me(current_user: userSchema.User = Depends(get_current_user)):
    return current_user


@app.post("/users/", response_model=userSchema.User)
def create_user(user: userSchema.UserCreate, db: Session = Depends(get_database_session)):
    # username validation
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    if len(user.username) < 3:
        raise HTTPException(status_code=400, detail="Username too short")
    if len(user.username) > 20:
        raise HTTPException(status_code=400, detail="Username too long")
    if not user.username:
        raise HTTPException(status_code=400, detail="Please key in a username")
    
    # email validation
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    if not user.email:
        raise HTTPException(status_code=400, detail="Please key in an email address")
    if '@' not in user.email:
        raise HTTPException(status_code=400, detail="Invalid email address")
    
    # password validation
    if len(user.password) < 8:
        raise HTTPException(status_code=400, detail="Password too short")
    if len(user.password) > 20:
        raise HTTPException(status_code=400, detail="Password too long")
    # if user.password.upper() == user.password:
    #     raise HTTPException(status_code=400, detail="Password must include lowercase letters")
    # if user.password.lower() == user.password:
    #     raise HTTPException(status_code=400, detail="Password must include uppercase letters")
    # if user.password.isalnum():
    #     raise HTTPException(status_code=400, detail="Password must have symbols")
    # if user.password.isalpha():
    #     raise HTTPException(status_code=400, detail="Password must have numbers")
    if not user.password:
        raise HTTPException(status_code=400, detail="Please key in a password")

    hashed_password = get_password_hash(user.password)
    return crud.create_user(db=db, user=user, hashed_password=hashed_password)


@app.get("/users/", response_model=list[userSchema.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_database_session)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=userSchema.User)
def read_user(user_id: int, db: Session = Depends(get_database_session)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.delete("/users/{user_id}", response_model=userSchema.User)
def delete_user(user_id: int, db: Session = Depends(get_database_session)):
    user = crud.get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return user



##End Authentication


#class for accessing URA api


@app.get("/cpColumns")
def col(db: Session = Depends(get_database_session)):
    return crud.get_carparks_basic_info(db)


@app.get("/rawCP")
def raw():
    return URA().getCarparks()

@app.post("/carpark/", response_model=Carpark)
def create_carpark(carpark: Carpark, db: Session = Depends(get_database_session)):
    return crud.create_carpark(db=db, carpark=carpark)


@app.get("/carpark/", response_model=list[Carpark])
def read_carparks(skip: int = 0, limit: int = -1, db: Session = Depends(get_database_session)):
    carparks = crud.get_carparks(db, skip=skip, limit=limit)
    return carparks

@app.get('/carparkByCode/{code}', response_model=Carpark)
def read_exact_carpark(code: str, db: Session = Depends(get_database_session)):
    return crud.get_carpark_by_code(db,code)

@app.get("/avail/")
async def getAvailCP():
    return URA().getAvailFinal()

@app.get("/search/{searchVal}")
async def getSearchResult(searchVal: str):
    return OneMap().getSearch(searchVal)

@app.get("/nearbyCP/{latLon}/{filterParam}/{reverse}")
async def getNearbyCP(latLon: str, filterParam: str, reverse: str, db: Session = Depends(get_database_session)):
    subjectCoor = latLon.split(',')
    if reverse == 'T':
        decreasing = True
    elif reverse == 'F':
        decreasing = False
    else:
        raise HTTPException(status_code=500, detail='revese must be T or F')
    try:
        carparks = crud.get_carparks(db = db)
        print(carparks)
        withinFiveMin = Filter().getNearby(carparks,subjectCoor)
        sorted = Filter().sort(filterParam, withinFiveMin, decreasing)
        return sorted
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)
    


    


# Import the Rocketry app
from scheduler import app as app_rocketry
from pydantic import BaseModel, Field, validator
session = app_rocketry.session

class Task(BaseModel):
    name: str
    description: Optional[str]
    priority: int

    start_cond: str
    end_cond: str
    timeout: Optional[int]

    disabled: bool
    force_termination: bool
    force_run: bool

    status: str
    is_running: bool
    last_run: Optional[datetime]
    last_success: Optional[datetime]
    last_fail: Optional[datetime]
    last_terminate: Optional[datetime]
    last_inaction: Optional[datetime]
    last_crash: Optional[datetime]

@app.get("/my-route")
async def get_tasks():
    return [
        Task(
            start_cond=str(task.start_cond), 
            end_cond=str(task.end_cond),
            is_running=task.is_running,
            **task.dict(exclude={'start_cond', 'end_cond'})
        )
        for task in session.tasks
    ]





# Booking endpoints
import db.schemas.bookingSchema as bookingSchema
import db.schemas.lotSchema as lotSchema
import db.schemas.favouriteSchema as favouriteSchema

@app.post("/booking/", response_model=bookingSchema.Booking)
def create_booking(booking: bookingSchema.BookingCreate,
                   db: Session = Depends(get_database_session),
                   current_user: userSchema.User = Depends(get_current_user)):
    b = crud.get_booking_by_attr(db=db, attribute="user_id", searchVal=current_user.id)
    if b is not None:
        raise HTTPException(status_code=400, detail="You cannot create 2 concurrent bookings")
    if not verify_booking_time(start_time=booking.start_time, end_time=booking.end_time):
        raise HTTPException(status_code=400, detail='The selected times are not valid')
    crud.update_lots(db,'id',booking.lot_id,'occupied',True)
    return crud.create_booking(db=db, booking=booking, user_id=current_user.id)


def verify_booking_time(start_time: str, end_time: str) -> bool:
    # CONSTANTS
    max_dist_to_start: timedelta = timedelta(hours=2)
    max_dist_to_end: timedelta = timedelta(hours=10)

    now = datetime.now() + timedelta(hours=8)
    start: datetime = time_str_to_datetime(start_time)
    #end: datetime = time_str_to_datetime(end_time)
    start_diff: timedelta = start - now
    #end_diff: timedelta = end - now
    #print(now, start, start_diff, end, end_diff)
    if start_diff > max_dist_to_start:# or end_diff > max_dist_to_end:
        return False
    return True


def time_str_to_datetime(time_str: str) -> datetime:
    # EXAMPLE STRING: 2023-04-08T12:35:00.000
    time_datetime: datetime = datetime(year=int(time_str[0:4]), month=int(time_str[5:7]),
                 day=int(time_str[8:10]), hour=int(time_str[11:13]),
                 minute=int(time_str[14:16]))
    return time_datetime


@app.get("/booking/", response_model=list[bookingSchema.Booking])
def read_bookings(skip: int = 0, limit: int = 100, db: Session = Depends(get_database_session)):
    booking = crud.get_bookings(db, skip=skip, limit=limit)
    return booking


@app.get("/booking/me/")
async def read_bookings_me(current_user: userSchema.User = Depends(get_current_user), db: Session = Depends(get_database_session)):
    bookings = current_user.bookings
    bookingList = []
    for booking in bookings:
        lotID = booking.lot_id
        lot : lotSchema.Lot = crud.get_lot_by_attr(db,'id',lotID)
        cp_code = lot.cp_code
        cp : Carpark = crud.get_carpark_by_code(db, cp_code)
        bookingInfo = {'booking': booking.__dict__, 'carpark': cp.__dict__}
        bookingList.append(bookingInfo)
    return bookingList


@app.delete("/booking/{booking_id}", response_model=bookingSchema.Booking)
def delete_booking(booking_id: int, db: Session = Depends(get_database_session), 
                current_user: userSchema.User = Depends(get_current_user)):
    booking = crud.get_booking_by_attr(db, attribute='id', searchVal=booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    crud.update_lots(db,'id',booking.lot_id,'occupied', False)
    db.delete(booking)
    db.commit()
    return booking



# Favourite endpoints
@app.post("/favourite/", response_model=favouriteSchema.Favourite)
def create_favourite(cp_code: str, favourite: favouriteSchema.FavouriteCreate,
                     db: Session = Depends(get_database_session),
                     current_user: userSchema.User = Depends(get_current_user)):
    return crud.create_favourite(db=db, favourite=favourite, 
                                 user_id=current_user.id, cp_code=cp_code)


@app.get("/favourite/", response_model=list[favouriteSchema.Favourite])
def read_favourites(skip: int = 0, limit: int = 100, db: Session = Depends(get_database_session)):
    favourites = crud.get_favourites(db, skip=skip, limit=limit)
    return favourites


@app.get("/favourite/me/", response_model=list[favouriteSchema.Favourite])
async def read_favourite_me(current_user: userSchema.User = Depends(get_current_user)):
    return current_user.favourites


@app.delete("/favourite/{favourite_id}", response_model=favouriteSchema.Favourite)
def delete_favourite(favourite_id: int, db: Session = Depends(get_database_session), 
                current_user: userSchema.User = Depends(get_current_user)):
    favourite = crud.get_favourites_by_attr(db, attribute='id', searchVal=favourite_id)
    if not favourite:
        raise HTTPException(status_code=404, detail="Favourite not found")
    db.delete(favourite)
    db.commit()
    return favourite



# Lot endpoints
@app.post("/lot/", response_model=lotSchema.Lot)
def create_lot(cp_code: str, lot: lotSchema.LotCreate, db: Session = Depends(get_database_session)):
    return crud.create_lot(db=db, lot=lot, cp_code=cp_code, occupied=False)


@app.get("/lot/", response_model=list[lotSchema.Lot])
def read_lots(skip: int = 0, limit: int = 100, db: Session = Depends(get_database_session)):
    lot = crud.get_lots(db, skip=skip, limit=limit)
    return lot


# @app.get("/lot_by_id/", response_model=list[lotSchema.Lot])
# def read_lots(skip: int = 0, limit: int = 100, db: Session = Depends(get_database_session)):
#     lot = crud.get_lots(db, skip=skip, limit=limit)
#     return lot



if __name__ == "__main__":
    app.run()
    print(os.getcwd())