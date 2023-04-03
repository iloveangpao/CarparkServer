from sqlalchemy.schema import Column
from typing import List
from sqlalchemy.types import String, Integer, Text, JSON, Boolean, ARRAY, PickleType, DateTime, Float
from sqlalchemy.dialects.mysql import MEDIUMTEXT, VARCHAR
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from db.database import Base
from datetime import datetime

class Carparks(Base):
    __tablename__ = "carparks"
    id = Column(Integer, index = True, autoincrement=True)
    cp_code = Column(VARCHAR(128), primary_key=True)
    name = Column(Text)
    locations = Column(PickleType)
    # Rates = Column(PickleType)
    rate = Column(Float)
    min = Column(Text)

    Availability = Column(Integer, nullable = True)
    

    lots = relationship("Lot", back_populates="carpark")
    favourites = relationship("Favourite", back_populates="carpark")

    #BookableSlots = Column(PickleType, nullable = True)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    email = Column(String(50), unique=True, index=True)
    hashed_password = Column(String(64))

    bookings = relationship("Booking", back_populates="user")
    favourites = relationship("Favourite", back_populates="user")


class Lot(Base):
    __tablename__ = "lots"

    id = Column(Integer, primary_key=True, index=True)
    cp_code = Column(VARCHAR(128), ForeignKey("carparks.cp_code"))

    carpark = relationship("Carparks", back_populates="lots")
    bookings = relationship("Booking", back_populates="lot")


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    start_time = Column(String(30), index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    lot_id = Column(Integer, ForeignKey("lots.id"))

    user = relationship("User", back_populates="bookings")
    lot = relationship("Lot", back_populates="bookings")
    
class Favourite(Base):
    __tablename__ = "favourites"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    carpark_id = Column(Integer, ForeignKey("carparks.id"))

    user = relationship("User", back_populates="favourites")
    carpark = relationship("Carparks", back_populates="favourites")