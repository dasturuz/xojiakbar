from sqlalchemy.orm import relationship

from db import Base
from sqlalchemy import *
class Tolov(Base):
    __tablename__ = "Tolov"
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    oquvchi_id = Column(Integer, nullable=False)
    fan_id = Column(Integer, nullable=False)
    oy = Column(String,nullable=False)
    narx = Column(Integer,nullable=False)
    turi = Column(String,nullable=False)
    date = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    status = Column(Boolean, default=True)
    user_id = Column(Integer,ForeignKey('Users.id'),nullable=False)
    owner = relationship('Users', back_populates='savdolar')