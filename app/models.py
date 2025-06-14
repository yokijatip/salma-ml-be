from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String)  # admin atau orang_tua

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    kelas = Column(String)
    
    # 12 Mata Pelajaran
    al_quran_iqro = Column(Integer)
    hafalan_surat_pendek = Column(Integer)
    hafalan_doa = Column(Integer)
    hafalan_ayat_pilihan = Column(Integer)
    bahasa_arab = Column(Integer)
    bahasa_inggris = Column(Integer)
    khat_menulis = Column(Integer)
    menggambar_mewarnai = Column(Integer)
    jasmani_kesehatan = Column(Integer)
    kreativitas_keaktifan = Column(Integer)
    ulumul_quran = Column(Integer)
    kemampuan_berbahasa = Column(Integer)
    
    # Calculated fields
    rata_rata = Column(Float)
    kategori = Column(String)
    
    # Foreign key
    orang_tua_id = Column(Integer, ForeignKey("users.id"))

    orang_tua = relationship("User")