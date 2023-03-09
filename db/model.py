from sqlalchemy.schema import Column
from sqlalchemy.types import String, Integer, Text, JSON
from database import Base

class Carparks(Base):
    __tablename__ = "carparks"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique = True)
    location = Column(JSON)
    Rates = Column(JSON, nullable = True)