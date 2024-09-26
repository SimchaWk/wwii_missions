from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from config.base import Base


class TargetType(Base):
    __tablename__ = 'target_types'

    target_type_id = Column(Integer, primary_key=True)
    target_type_name = Column(String(255), unique=True, nullable=False)

    targets = relationship("Target", back_populates="target_type")
