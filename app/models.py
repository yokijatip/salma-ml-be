from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String)  # admin atau orang_tua



# Table untuk menyimpan data Siswa
class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    kelas = Column(String)
    tanggal_lahir = Column(String)  # Format YYYY-MM-DD
    jenis_kelamin = Column(String)  # Laki-laki atau Perempuan
    no_hp = Column(String)  # Nomor handphone
    nama_orang_tua = Column(String)  # Nama orang tua
    
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

# Table untuk menyimpan informasi kegiatan
class Kegiatan(Base):
    __tablename__ = "kegiatan"

    id = Column(Integer, primary_key=True, index=True)
    nama_kegiatan = Column(String, index=True)
    deskripsi = Column(String)
    tanggal = Column(String)  # Format YYYY-MM-DD
    kelas = Column(String)  # Kelas yang mengikuti kegiatan
    waktu_mulai = Column(String)  # Format HH:MM
    waktu_selesai = Column(String)  # Format HH:MM
    lokasi = Column(String)
    fotoKegiatan = Column(String)  # URL atau path ke foto kegiatan

    # Foreign key untuk mengaitkan dengan User (admin)
    admin_id = Column(Integer, ForeignKey("users.id"))
    admin = relationship("User")  # Relasi ke User sebagai admin kegiatan


# Table untuk menyimpan data pengumuman

class Pengumuman(Base):
    __tablename__ = "pengumuman"

    id = Column(Integer, primary_key=True, index=True)
    nama_pengumuman = Column(String, index=True)
    deskripsi = Column(String)
    tanggal = Column(String)  # Format YYYY-MM-DD
    kelas = Column(String)
    waktu_mulai = Column(String)  # Format HH:MM
    waktu_selesai = Column(String)  # Format HH:MM
    lokasi = Column(String)
    fotoPengumuman = Column(String)  # URL atau path ke foto pengumuman

    # Foreign key untuk mengaitkan dengan User (admin)
    admin_id = Column(Integer, ForeignKey("users.id"))
    admin = relationship("User")  # Relasi ke User sebagai admin Pengumuman