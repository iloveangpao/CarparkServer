from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "mysql+mysqlconnector://root@localhost:3306/my-db"
engine = create_engine(DATABASE_URL)

#create session for eliminating security issues
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

##use to create database model
Base = declarative_base()