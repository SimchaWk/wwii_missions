from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy_utils import database_exists, create_database

from config.base import Base


class City(Base):
    __tablename__ = 'cities'

    city_id = Column(Integer, primary_key=True)
    city_name = Column(String(100), unique=True, nullable=False)
    country_id = Column(Integer, ForeignKey('countries.country_id'), nullable=False)
    latitude = Column(Float)
    longitude = Column(Float)

    country = relationship("Country", back_populates="cities")
    targets = relationship("Target", back_populates="city")
