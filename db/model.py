from sqlalchemy.schema import Column
from typing import List
from sqlalchemy.types import String, Integer, Text, JSON, Boolean, ARRAY, PickleType, DateTime
from sqlalchemy.dialects.mysql import MEDIUMTEXT, VARCHAR
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from db.database import Base
from datetime import datetime

class Carparks(Base):
    __tablename__ = "carparks"
    id = Column(Integer, primary_key=True, index = True)
    cp_code = Column(Text)
    name = Column(Text)
<<<<<<< HEAD
    locations = Column(PickleType)
    Rates = Column(PickleType)
=======
    locations = Column(JSON)
    Rates = Column(JSON)
    
    lots = relationship("Lot", back_populates="carpark")
>>>>>>> e846c2a499b6b225e1cfb85975798c4d0cb42659

    #BookableSlots = Column(PickleType, nullable = True)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    email = Column(String(50), unique=True, index=True)
    hashed_password = Column(String(64))

    bookings = relationship("Booking", back_populates="user")


class Lot(Base):
    __tablename__ = "lots"

    id = Column(Integer, primary_key=True, index=True)
    carpark_id = Column(Integer, ForeignKey("carparks.id"))

    carpark = relationship("Carparks", back_populates="lots")
    bookings = relationship("Booking", back_populates="lot")


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    start_time = Column(DateTime, default=datetime.utcnow)
    end_time = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"))
    lot_id = Column(Integer, ForeignKey("lots.id"))

    user = relationship("User", back_populates="bookings")
    lot = relationship("Lot", back_populates="bookings")
    
