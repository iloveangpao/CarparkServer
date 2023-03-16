from sqlalchemy.schema import Column
from sqlalchemy.types import String, Integer, Text, JSON
from sqlalchemy.dialects.mysql import MEDIUMTEXT, VARCHAR
from db.database import Base

class Carparks(Base):
    __tablename__ = "carparks"
    id = Column(Integer, primary_key=True, index = True)
    cp_code = Column(Text)
    name = Column(Text)
    locations = Column(JSON, nullable = True)
    Rates = Column(JSON, nullable = True)


class Users(Base):
    __tablename__ = "users"
    username = Column(VARCHAR(128), primary_key = True)
    hashed_password = Column(Text)