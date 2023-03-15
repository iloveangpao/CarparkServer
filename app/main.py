import sys
sys.path.append('/code/')
import asyncio
import uvicorn
sys.stdout = Unbuffered(sys.stdout)

from fastapi import Depends, FastAPI, HTTPException, status, Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
import json

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hellop World"}

@app.get("/asdf")
async def new():
    return {"new": "here"}

from datetime import datetime, timedelta
from db.schemas.userSchema import *
from db.database import SessionLocal, engine
import db.model as model
from sqlalchemy.orm import Session
from sqlalchemy import select

model.Base.metadata.create_all(bind=engine)

def get_database_session():
    db = SessionLocal()
    try:
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
from app.ura import URA
from db.schemas.carparkSchema import *
import db.crud as crud

import os
print(os.getcwd())


'''will clean this shit up later'''
# db stuff
# @app.get("/carparks", response_model=Carpark)
# async def create_carpark(db: Session = Depends(get_database_session), carparkData: json = None):
#     ura = URA(1)
#     carparks = ura.getCarparks()

#     # for cp in carparks:
#     #     for item in cp.items():
#     #         print(item)
#     #     print()
#     cp = carparks[0]    
#     r = Rate(
#         weekdayMin=cp['weekdayMin'],
#         endTime=cp['endTime'],
#         weekdayRate=cp['weekdayRate'],
#         startTime=cp['startTime'],
#         sunPHRate=cp['sunPHRate'],
#         sunPHMin=cp['sunPHMin'],
#         satdayRate=cp['satdayRate'],
#         satdayMin=cp['satdayMin']
#     )
#     l = Location(
#         num=len(cp['geometries']),
#         locations=[tuple(map(float, loc.split(','))) for loc in cp['geometries']]
#     )
#     carpark = Carpark(id=cp['ppCode'], name=cp['ppName'], locations=l, Rates=r)
#     db.add(carpark)
#     db.commit()
    
#     print("added carpark")
#     return db.query(Carpark).offset(0).limit(100).all()

'''this is the impt stuff for rn'''
@app.post("/carpark/", response_model=Carpark)
def create_carpark(carpark: CarparkCreate, db: Session = Depends(get_database_session)):
    return crud.create_user(db=db, carpark=carpark)


@app.get("/carpark/", response_model=list[Carpark])
def read_carparks(skip: int = 0, limit: int = 100, db: Session = Depends(get_database_session)):
    carparks = crud.get_carparks(db, skip=skip, limit=limit)
    return carparks
    
from app.fastAPIApp import app as app_fastapi
from scheduler import app as app_rocketry


class Server(uvicorn.Server):
    """Customized uvicorn.Server

    Uvicorn server overrides signals and we need to include
    Rocketry to the signals."""
    def handle_exit(self, sig: int, frame) -> None:
        app_rocketry.session.shut_down()
        return super().handle_exit(sig, frame)


async def main():
    "Run scheduler and the API"
    server = Server(config=uvicorn.Config(app_fastapi, host = '0.0.0.0', port = 8000, workers=1, loop="asyncio"))

    api = asyncio.create_task(server.serve())
    sched = asyncio.create_task(app_rocketry.serve())

    await asyncio.wait([sched, api])

if __name__ == "__main__":
    asyncio.run(main())