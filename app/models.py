from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String) #admin atau orang_tua

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    nilai_1 = Column(Integer)
    nilai_2 = Column(Integer)
    nilai_3 = Column(Integer)
    nilai_4 = Column(Integer)
    orang_tua_id = Column(Integer, ForeignKey("users.id"))

    orang_tua = relationship("User")