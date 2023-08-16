from sqlalchemy.orm import relationship

from db import Base
from sqlalchemy import *
class Kurslar(Base):
    __tablename__ = "Kurslar"
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    oqtuvchi_id = Column(Integer, nullable=False)
    fan_id = Column(Integer, nullable=False)
    soat = Column(String, nullable=False)
    kurs_muddati = Column(Integer,nullable=False)
    xona = Column(Integer, nullable=False)
    date = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    status = Column(Boolean, default=True)
    user_id = Column(Integer,ForeignKey('Users.id'),nullable=False)
    owner = relationship('Users', back_populates='soti')