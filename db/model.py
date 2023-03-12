from sqlalchemy.schema import Column
from sqlalchemy.types import String, Integer, Text, JSON
from db.database import Base

class Carparks(Base):
    __tablename__ = "carparks"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(Text)
    locations = Column(JSON, nullable = True)
    Rates = Column(JSON, nullable = True)