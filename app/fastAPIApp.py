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

from fastapi import Depends, FastAPI, HTTPException, status
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
print(os.listdir())
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

###Authentication
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

User = User()

def fake_hash_password(password: str):
    return "fakehashed" + password


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)

async def get_user(db: SessionLocal, username: str) -> model.Users:
    result = await db.execute(select(model.Users).filter_by(username=username))
    return result.scalars().first()


async def authenticate_user(db : SessionLocal, username: str, password: str) -> model.Users:
    user = await get_user(db , username)
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


async def get_current_user(db : SessionLocal = Depends(get_database_session) , token: str = Depends(oauth2_scheme)) -> model.Users:
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
    user = await get_user(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.post("/token", response_model=Token)
async def login_for_access_token(db : SessionLocal = Depends(get_database_session) , form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(db, form_data.username, form_data.password)
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


@app.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


##End Authentication


#class for accessing URA api
import sys
print(sys.path)
print(os.listdir())
from app.ura import URA

import os
print(os.getcwd())

# db stuff


def create_carpark(db: Session = Depends(get_database_session), carparkData : json = None):
    carpark = model.Carparks(
        id = carparkData["ppCode"],
        name = carparkData["ppName"],
        locations = carparkData[""]
    )
    db.add(carpark)
    db.commit()

###making endpoint

# @app.get("/carparkInfo/{requirement}")

# async def carpark(requirement):
#     uraGetter = URA()
#     getter = getattr(uraGetter, requirement)
#     result = getter()
#     return {requirement : result}

# @app.get("/items/{item_id}")

# def read_item(item_id : int , q: Union[str,None] = None):
#     return {"item_id": item_id, "q": q}

@app.get("/carparkInfo")
async def read_movies(db: Session = Depends(get_database_session)):
    carparkData = URA.getCarparks()
    carpark = model.Carparks(
        id = carparkData["ppCode"],
        name = carparkData["ppName"],
        locations = carparkData[""]
    )
    db.add(carpark)
    db.commit()
    records = db.query(Carparks).all()
    return records




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

# @app.post("/my-route")
# async def manipulate_session():
#     for task in session.tasks:
#         ...






if __name__ == "__main__":
    app.run()
    print(os.getcwd())