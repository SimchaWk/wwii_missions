from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship

from config.base import Base


class Country(Base):
    __tablename__ = 'countries'

    country_id = Column(Integer, primary_key=True)
    country_name = Column(String(100), unique=True, nullable=False)

    cities = relationship("City", back_populates="country")
