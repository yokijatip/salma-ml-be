from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import Base, engine, SessionLocal
from . import models, auth
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from typing import List
from .ml_model import predict_performance
from typing import List

# Untuk menjalankan server local menggunakan uvicorn 
# uvicorn app.main:app --reload

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Schemas
class UserCreate(BaseModel):
    username: str
    password: str
    role: str  # "admin" atau "orang_tua"


class UserResponse(BaseModel):
    id: int
    username: str
    role: str

    class Config:
        orm_mode = True

class StudentBase(BaseModel):
    name: str
    kelas: str
    tanggal_lahir: str  # Format YYYY-MM-DD
    jenis_kelamin: str  # Laki-laki atau Perempuan
    no_hp: str
    nama_orang_tua: str
    al_quran_iqro: int
    hafalan_surat_pendek: int
    hafalan_doa: int
    hafalan_ayat_pilihan: int
    bahasa_arab: int
    bahasa_inggris: int
    khat_menulis: int
    menggambar_mewarnai: int
    jasmani_kesehatan: int
    kreativitas_keaktifan: int
    ulumul_quran: int
    kemampuan_berbahasa: int

class StudentCreate(StudentBase):
    orang_tua_id: int


class StudentResponse(StudentBase):
    id: int
    rata_rata: float
    kategori: str
    orang_tua_id: int

    class Config:
        orm_mode = True

class PredictRequest(BaseModel):
    al_quran_iqro: int
    hafalan_surat_pendek: int
    hafalan_doa: int
    hafalan_ayat_pilihan: int
    bahasa_arab: int
    bahasa_inggris: int
    khat_menulis: int
    menggambar_mewarnai: int
    jasmani_kesehatan: int
    kreativitas_keaktifan: int
    ulumul_quran: int
    kemampuan_berbahasa: int

class PredictResponse(BaseModel):
    kategori: str

# Kegiatan schemas
class KegiatanBase(BaseModel):
    nama_kegiatan: str
    deskripsi: str
    tanggal: str  # Format YYYY-MM-DD
    kelas: str  # Kelas yang mengikuti kegiatan
    waktu_mulai: str  # Format HH:MM
    waktu_selesai: str  # Format HH:MM
    lokasi: str
    fotoKegiatan: str  # URL atau path ke foto kegiatan

# Create Kegiatan
class KegiatanCreate(KegiatanBase):
    pass

class KegiatanResponse(KegiatanBase):
    id: int
    pass

    class Config:
        orm_mode = True

class KegiatanListResponse(BaseModel):
    kegiatan: List[KegiatanResponse]

    class Config:
        orm_mode = True

# Pengumuman schemas
class PengumumanBase(BaseModel):
    nama_pengumuman: str
    deskripsi: str
    tanggal: str  # Format YYYY-MM-DD
    kelas: str  # Kelas yang mengikuti kegiatan
    waktu_mulai: str  # Format HH:MM
    waktu_selesai: str  # Format HH:MM
    lokasi: str
    fotoPengumuman: str  # URL atau path ke foto kegiatan

# Create Kegiatan
class PengumumanCreate(PengumumanBase):
    pass

class PengumumanResponse(PengumumanBase):
    id: int
    pass

    class Config:
        orm_mode = True

class PengumumanListResponse(BaseModel):
    pengumuman: List[PengumumanResponse]

    class Config:
        orm_mode = True



def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> models.User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Tidak dapat memvalidasi token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = db.query(models.User).filter(models.User.username == username).first()
    if user is None:
        raise credentials_exception
    return user

def calculate_average_and_category(student_data):
    """
    Menghitung rata-rata dan kategori berdasarkan 12 mata pelajaran
    """
    # Ambil semua nilai mata pelajaran (exclude name, kelas, orang_tua_id)
    subjects = [
        student_data.al_quran_iqro,
        student_data.hafalan_surat_pendek,
        student_data.hafalan_doa,
        student_data.hafalan_ayat_pilihan,
        student_data.bahasa_arab,
        student_data.bahasa_inggris,
        student_data.khat_menulis,
        student_data.menggambar_mewarnai,
        student_data.jasmani_kesehatan,
        student_data.kreativitas_keaktifan,
        student_data.ulumul_quran,
        student_data.kemampuan_berbahasa
    ]
    
    # Hitung rata-rata
    rata_rata = sum(subjects) / len(subjects)
    
    # Tentukan kategori
    if rata_rata >= 85:
        kategori = "BSB"
    elif rata_rata >= 70:
        kategori = "BSH"
    elif rata_rata >= 60:
        kategori = "MB"
    else:
        kategori = "BB"
    
    return round(rata_rata, 2), kategori


# Register
@app.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username sudah terdaftar")
    hashed_password = auth.get_password_hash(user.password)
    new_user = models.User(username=user.username, hashed_password=hashed_password, role=user.role)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "Registrasi berhasil"}

# Login
@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Login gagal")
    
    access_token = auth.create_access_token(data={"sub": user.username, "role": user.role})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/me", response_model=UserResponse)
def read_users_me(current_user: models.User = Depends(get_current_user)):
    return current_user



# Fungsi untuk membuat data siswa
@app.post("/students", response_model=StudentResponse)
def create_student(student: StudentCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Hanya admin yang bisa menambah data siswa")
    
    # Hitung rata-rata dan kategori
    rata_rata, kategori = calculate_average_and_category(student)
    
    # Buat student baru
    student_dict = student.dict()
    student_dict["rata_rata"] = rata_rata
    student_dict["kategori"] = kategori
    
    new_student = models.Student(**student_dict)
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student

# Fungsi untuk mengambil semua data siswa
@app.get("/students", response_model=List[StudentResponse])
def get_students(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return db.query(models.Student).all()

# Fungsi untuk menghitung jumlah siswa (HARUS SEBELUM /students/{id})
@app.get("/students/count")
def get_students_count(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Hanya admin yang bisa melihat jumlah siswa")
    
    total_students = db.query(models.Student).count()
    return {"total_students": total_students}

# Fungsi untuk mengambil data siswa berdasarkan ID
@app.get("/students/{id}", response_model=StudentResponse)
def get_student_by_id(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    student = db.query(models.Student).filter(models.Student.id == id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Siswa tidak ditemukan")
    
    # Jika role orang_tua, hanya boleh akses miliknya sendiri
    if current_user.role == "orang_tua" and student.orang_tua_id != current_user.id:
        raise HTTPException(status_code=403, detail="Akses ditolak")
    
    return student

# Fungsi untuk mengupdate data siswa
@app.put("/students/{id}", response_model=StudentResponse)
def update_student(id: int, updated: StudentBase, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Hanya admin yang bisa edit data siswa")

    student = db.query(models.Student).filter(models.Student.id == id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Siswa tidak ditemukan")

    # Hitung rata-rata dan kategori yang baru
    rata_rata, kategori = calculate_average_and_category(updated)
    
    # Update semua field
    for key, value in updated.dict().items():
        setattr(student, key, value)
    
    # Set rata-rata dan kategori
    student.rata_rata = rata_rata
    student.kategori = kategori

    db.commit()
    db.refresh(student)
    return student

# Fungsi untuk menghapus data siswa
@app.delete("/students/{id}")
def delete_student(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Hanya admin yang bisa menghapus data siswa")

    student = db.query(models.Student).filter(models.Student.id == id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Siswa tidak ditemukan")

    db.delete(student)
    db.commit()
    return {"message": "Data siswa berhasil dihapus"}


# Fungsi untuk membuat kegiatan
@app.post("/kegiatan", response_model=KegiatanResponse)
def create_kegiatan(kegiatan: KegiatanCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Hanya admin yang bisa menambah kegiatan")
    
    new_kegiatan = models.Kegiatan(**kegiatan.dict(), admin_id=current_user.id)
    db.add(new_kegiatan)
    db.commit()
    db.refresh(new_kegiatan)
    return new_kegiatan

# Fungsi untuk mengambil semua kegiatan
@app.get("/kegiatan", response_model=KegiatanListResponse)
def get_kegiatan(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    kegiatan_list = db.query(models.Kegiatan).all()
    return {"kegiatan": kegiatan_list}


# Fungsi untuk mengambil kegiatan berdasarkan ID
@app.get("/kegiatan/{id}", response_model=KegiatanResponse)
def get_kegiatan_by_id(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    kegiatan = db.query(models.Kegiatan).filter(models.Kegiatan.id == id).first()
    if not kegiatan:
        raise HTTPException(status_code=404, detail="Kegiatan tidak ditemukan")
    return kegiatan

# Fungsi untuk mengupdate kegiatan
@app.put("/kegiatan/{id}", response_model=KegiatanResponse)
def update_kegiatan(id: int, updated: KegiatanBase, db: Session = Depends
(get_db), current_user: models.User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Hanya admin yang bisa mengedit kegiatan")

    kegiatan = db.query(models.Kegiatan).filter(models.Kegiatan.id == id).first()
    if not kegiatan:
        raise HTTPException(status_code=404, detail="Kegiatan tidak ditemukan")

    for key, value in updated.dict().items():
        setattr(kegiatan, key, value)

    db.commit()
    db.refresh(kegiatan)
    return kegiatan

# Fungsi untuk menghapus kegiatan
@app.delete("/kegiatan/{id}")
def delete_kegiatan(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Hanya admin yang bisa menghapus kegiatan")

    kegiatan = db.query(models.Kegiatan).filter(models.Kegiatan.id == id).first()
    if not kegiatan:
        raise HTTPException(status_code=404, detail="Kegiatan tidak ditemukan")

    db.delete(kegiatan)
    db.commit()
    return {"message": "Kegiatan berhasil dihapus"}

# Pengumuman CRUD
# Fungsi untuk membuat Pengumuman
@app.post("/pengumuman", response_model=PengumumanResponse)
def create_pengumuman(
    pengumuman: PengumumanCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403, detail="Hanya admin yang bisa menambah pengumuman"
        )

    new_pengumuman = models.Pengumuman(**pengumuman.dict(), admin_id=current_user.id)
    db.add(new_pengumuman)
    db.commit()
    db.refresh(new_pengumuman)
    return new_pengumuman


# Fungsi untuk mengambil semua Pengumuman
@app.get("/pengumuman", response_model=PengumumanListResponse)
def get_pengumuman(
    db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)
):
    pengumuman_list = db.query(models.Pengumuman).all()
    return {"pengumuman": pengumuman_list}


# Fungsi untuk mengambil Pengumuman berdasarkan ID
@app.get("/pengumuman/{id}", response_model=PengumumanResponse)
def get_pengumuman_by_id(
    id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    pengumuman = db.query(models.Pengumuman).filter(models.Pengumuman.id == id).first()
    if not pengumuman:
        raise HTTPException(status_code=404, detail="pengumuman tidak ditemukan")
    return pengumuman


# Fungsi untuk mengupdate Pengumuman
@app.put("/pengumuman/{id}", response_model=PengumumanResponse)
def update_pengumuman(
    id: int,
    updated: PengumumanBase,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403, detail="Hanya admin yang bisa mengedit pengumuman"
        )

    pengumuman = db.query(models.Pengumuman).filter(models.Pengumuman.id == id).first()
    if not pengumuman:
        raise HTTPException(status_code=404, detail="pengumuman tidak ditemukan")

    for key, value in updated.dict().items():
        setattr(pengumuman, key, value)

    db.commit()
    db.refresh(pengumuman)
    return pengumuman


# Fungsi untuk menghapus Pengumuman
@app.delete("/pengumuman/{id}")
def delete_pengumuman(
    id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403, detail="Hanya admin yang bisa menghapus pengumuman"
        )

    pengumuman = db.query(models.Pengumuman).filter(models.Pengumuman.id == id).first()
    if not pengumuman:
        raise HTTPException(status_code=404, detail="pengumuman tidak ditemukan")

    db.delete(pengumuman)
    db.commit()
    return {"message": "pengumuman berhasil dihapus"}


# Fungsi untuk melakukan prediksi
@app.post("/predict", response_model=PredictResponse)
def predict(data: PredictRequest, current_user: models.User = Depends(get_current_user)):
    result = predict_performance(
        data.al_quran_iqro,
        data.hafalan_surat_pendek,
        data.hafalan_doa,
        data.hafalan_ayat_pilihan,
        data.bahasa_arab,
        data.bahasa_inggris,
        data.khat_menulis,
        data.menggambar_mewarnai,
        data.jasmani_kesehatan,
        data.kreativitas_keaktifan,
        data.ulumul_quran,
        data.kemampuan_berbahasa
    )
    return {"kategori": result}