from sqlalchemy.orm import relationship

from db import Base
from sqlalchemy import *
class Oqtuvchi(Base):
    __tablename__ = "Oqtuvchi"
    id = Column(Integer,primary_key=True,nullable=False,autoincrement=True)
    ism = Column(String(20), nullable=False)
    familya = Column(String(20),nullable=False)
    tel = Column(Integer, nullable=False)
    roll = Column(String(20), nullable=False)
    fan_id = Column(Integer, nullable=False)
    password = Column(Integer, nullable=False)
    username = Column(String(20), unique=True, nullable=False)
    status = Column(Boolean, default=True)
    user_id = Column(Integer,ForeignKey('Users.id'),nullable=False)
    date = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    token = Column(String(400), default='', nullable=True)
    owner = relationship('Users', back_populates='sot')

