from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from urllib import parse

## specify database configs
config = {
    'host' : '0.0.0.0',
    'port' : 3306,
    'user' : 'root',
    'password' : 'password',
    'database' : 'carpakdb'
}

db_user = config.get('user')
db_pwd = config.get('password')
db_host = config.get('host')
db_port = config.get('port')
db_name = config.get('database')

DATABASE_URL = f'mysql+pymysql://{db_user}:{db_pwd}@{db_host}:{db_port}/{db_name}'
engine = create_engine(DATABASE_URL, pool_timeout=20, pool_recycle=299)

#create session for eliminating security issues
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

##use to create database model
Base = declarative_base()