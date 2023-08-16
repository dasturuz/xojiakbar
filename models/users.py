from sqlalchemy import Column, Integer, String, Boolean,Float,Text
from sqlalchemy.orm import relationship

from db import Base




class Users(Base):
    __tablename__ = "Users"
    id = Column(Integer, primary_key=True)
    roll = Column(String(20), nullable=False)
    name = Column(String(20), nullable=False)
    number = Column(String(20), nullable=False)
    username = Column(String(20), unique=True, nullable=False)
    password = Column(String(200), nullable=False)
    status = Column(Boolean, nullable=False, default=True)
    token = Column(String(400), default='',nullable=True)
    savdo = relationship('Xona', back_populates='owner')
    savdolar = relationship('Tolov', back_populates='owner')
    sotish = relationship('Oquvchi', back_populates='owner')
    sot = relationship('Oqtuvchi', back_populates='owner')
    sotil = relationship('Kurssanalri', back_populates='owner')
    soti = relationship('Kurslar', back_populates='owner')
    so = relationship('Fanlar', back_populates='owner')
    s = relationship('Chiqimlar', back_populates='owner')



