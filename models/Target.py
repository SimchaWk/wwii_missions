from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship

from config.base import Base


class Target(Base):
    __tablename__ = 'targets'

    target_id = Column(Integer, primary_key=True)
    target_industry = Column(String(255), nullable=False)
    city_id = Column(Integer, ForeignKey('cities.city_id'), nullable=False)
    target_type_id = Column(Integer, ForeignKey('target_types.target_type_id'))
    target_priority = Column(Integer)

    city = relationship("City", back_populates="targets")
    target_type = relationship("TargetType", back_populates="targets")
