from sqlalchemy import Column, DateTime, String, Integer, Date, Table, UniqueConstraint, ForeignKey, Boolean, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

Orders = Table('orders', Base.metadata,
               Column('plant_culture_id', Integer, ForeignKey('plant_culture.id')),
               Column('user_id', Integer, ForeignKey('user.id')),
               Column('status', String)
               )


class PlantCulture(Base):
    __tablename__ = 'plant_culture'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Integer)
    description = Column(String)

    orders = relationship('User', secondary=Orders, backref='PlantCulture')


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    user_name = Column(String)
    first_name = Column(String)
    last_name = Column(String)

    orders = relationship('PlantCulture', secondary=Orders, backref='User')

    def __init__(self, user):
        self.id = user.id
        self.user_name = user.username
        self.first_name = user.first_name
        self.last_name = user.last_name
