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

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}



from datetime import datetime, timedelta
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


model.Base.metadata.create_all(bind=engine)

def get_database_session():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

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
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
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


##End Authentication


#class for accessing URA api
from app.ura import URA
from db.schemas.carparkSchema import *
import db.crud as crud
import os, json

@app.post("/carpark/", response_model=Carpark)
def create_carpark(carpark: Carpark, db: Session = Depends(get_database_session)):
    return crud.create_carpark(db=db, carpark=carpark)


@app.get("/carpark/", response_model=list[Carpark])
def read_carparks(skip: int = 0, limit: int = 100, db: Session = Depends(get_database_session)):
    carparks = crud.get_carparks(db, skip=skip, limit=limit)
    carparkList = []
    for i in carparks:
        print(i.locations)
        print(type(i.locations))
        # test = json.loads(i.locations)
        # print(test)

        carparkList.append(Carpark(id = i.id, cp_code = i.cp_code, name = i.name, locations = i.locations, Rates = i.Rates, BookableSlots = i.BookableSlots))
    return carparks

@app.get("/avail/")
async def getAvailCP():
    avails = URA().getAvail()
    from SVYconverter import SVY21

    for i in range(len(avails)):
        temp = avails[i]
        tempCoor = temp['geometries']
        newCoor = []
        for j in tempCoor:
            tempLatLon = [float(k) for k in j['coordinates'].split(',')]
            print(tempLatLon)
            convert = SVY21().computeLatLon(tempLatLon[0],tempLatLon[1])
            print(convert)
            newCoor.append({'coordinates':'%s,%s'%(convert[0],convert[1])})
        print(newCoor)
        avails[i]['geometries'] = newCoor

    print(avails)
    return avails


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


if __name__ == "__main__":
    app.run()
    print(os.getcwd())