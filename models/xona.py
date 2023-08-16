from sqlalchemy.orm import relationship

from db import Base
from sqlalchemy import *
class Xona(Base):
    __tablename__ = "Xona"
    id = Column(Integer,primary_key=True,nullable=False,autoincrement=True)
    xona_nomi = Column(String(20), nullable=False)
    raqami = Column(Integer, nullable=False)
    status = Column(Boolean, default=True)
    date = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    user_id = Column(Integer,ForeignKey('Users.id'),nullable=False)
    owner = relationship('Users', back_populates='savdo')
