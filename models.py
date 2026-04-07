from sqlalchemy import Column, String, Integer, Float
from database import Base

class Patient(Base):
    __tablename__ = "patients"

    id = Column(String, primary_key=True)
    name = Column(String)
    city = Column(String)
    age = Column(Integer)
    gender = Column(String)
    height = Column(Float)
    weight = Column(Float)