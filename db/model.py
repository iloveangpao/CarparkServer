from sqlalchemy.schema import Column
from sqlalchemy.types import String, Integer, Text, JSON, Boolean
from sqlalchemy.dialects.mysql import MEDIUMTEXT, VARCHAR
from sqlalchemy.orm import relationship
from db.database import Base

class Carparks(Base):
    __tablename__ = "carparks"
    id = Column(Integer, primary_key=True, index = True)
    cp_code = Column(Text)
    name = Column(Text)
    locations = Column(JSON, nullable = True)
    Rates = Column(JSON, nullable = True)


'''class Users(Base):
    __tablename__ = "users"
    username = Column(VARCHAR(128), primary_key = True)
    hashed_password = Column(Text)'''


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(50), unique=True, index=True)
    email = Column(String(50), unique=True, index=True)
    # phone = Column(String, unique=True, index=True)
    hashed_password = Column(String(64))
    # disabled = Column(Boolean, default=False, index=True) # dont know if we actually need this, was giving errors jn, but pretty sure this isn't necessary

    # bookings = relationship("bookings", back_populates="owner") # bookings is the name of the booking __tablename__ and owner is the attribute that links it to a user