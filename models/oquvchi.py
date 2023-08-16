from sqlalchemy.orm import relationship

from db import Base
from sqlalchemy import *
class Oquvchi(Base):
    __tablename__ = "Oquvchi"
    id = Column(Integer,primary_key=True,nullable=False,autoincrement=True)
    ism = Column(String(20), nullable=False)
    familya = Column(String(20),nullable=False)
    yosh = Column(Integer, nullable=False)
    tel = Column(Integer, nullable=False)
    address = Column(String(50), nullable=False)
    fan = Column(String, nullable=False)
    soat = Column(String, nullable=False)
    date = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    status = Column(Boolean, default=True)
    user_id = Column(Integer,ForeignKey('Users.id'),nullable=False)
    owner = relationship('Users', back_populates='sotish')