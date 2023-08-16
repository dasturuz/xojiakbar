from sqlalchemy.orm import relationship

from db import Base
from sqlalchemy import *
class Kurssanalri(Base):
    __tablename__ = "Kurssanalri"
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    oqtuvchi_id = Column(Integer, nullable=False)
    fan_id = Column(Integer, nullable=False)
    xona_id = Column(Integer, nullable=False)
    bor = Column(String, nullable=False)
    yoq = Column(String, nullable=False)
    boshi = Column(String, nullable=False)
    oxiri = Column(String, nullable=False)
    oquvchi_id = Column(Integer, nullable=False)
    user_id = Column(Integer,ForeignKey('Users.id'),nullable=False)
    soat = Column(String, nullable=False)
    kurs_muddati = Column(Integer,nullable=False)
    date = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    status = Column(Boolean, default=True)
    owner = relationship('Users', back_populates='sotil')