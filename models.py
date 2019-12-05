from sqlalchemy import Column, DateTime, String, Integer, Date, Table, UniqueConstraint, ForeignKey, Boolean, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class PlantCulture(Base):
    __tablename__ = 'plant_culture'
    name = Column(String)
    price = Column(Integer)
    description = Column(String)
