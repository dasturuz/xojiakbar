from sqlalchemy.orm import relationship

from db import Base
from sqlalchemy import *
class Chiqimlar(Base):
    __tablename__ = "Chiqimlar"
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    oqtuvchi_id = Column(Integer, nullable=False)
    pul = Column(Integer,nullable=False)
    turi = Column(String,nullable=False)
    comment = Column(String(100), nullable=True)
    user_id = Column(Integer,ForeignKey('Users.id'),nullable=False)
    date = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    status = Column(Boolean, default=True)
    owner = relationship('Users', back_populates='s')