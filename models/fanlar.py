from sqlalchemy.orm import relationship

from db import Base
from sqlalchemy import *
class Fanlar(Base):
    __tablename__ = "Fanlar"
    id = Column(Integer,primary_key=True,nullable=False,autoincrement=True)
    nomi = Column(String(20), nullable=False)
    user_id = Column(Integer,ForeignKey('Users.id'),nullable=False)
    status = Column(Boolean, default=True)
    date = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    owner = relationship('Users', back_populates='so')