from sqlalchemy import Column, DateTime, String, Integer, Float, ForeignKey, func
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
  
class Characteristics(Base):
    __tablename__ = 'characteristics'
    id = Column(Integer, primary_key=True)
    manufacturer = Column(String)
    brand = Column(String)
    weight = Column(Float)
    volume = Column(Float)
    score = Column(Float)
    
class Product(Base):
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Float)
    collected_on = Column(DateTime, default=func.now())
    char = relationship(Characteristics, backref=backref('product', uselist=True))
    char_id = Column(Integer, ForeignKey('characteristics.id'))
