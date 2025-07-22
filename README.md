# salma-ml-be

**Sistem Backend Machine Learning untuk Evaluasi Performa Siswa TPQ menggunakan FastAPI dan Random Forest Classifier**

---

## 📌 Deskripsi

Proyek ini adalah backend berbasis Python (FastAPI) yang memanfaatkan algoritma Machine Learning (Random Forest Classifier) untuk memprediksi performa siswa pada lembaga pendidikan TPQ (Taman Pendidikan Al-Quran). Sistem ini memungkinkan:

- Admin mengelola data siswa
- Orang tua melihat hasil evaluasi anaknya
- Prediksi performa siswa otomatis berdasarkan 12 parameter nilai
- Evaluasi performa model (akurasi, confusion matrix, dll)
- Manajemen kegiatan dan pengumuman TPQ
- Sistem autentikasi berbasis JWT dengan role-based access

---

## ⚙️ Teknologi yang Digunakan

- **FastAPI** - Web framework Python
- **Scikit-Learn** - Machine Learning (Random Forest)
- **SQLite + SQLAlchemy** - Database lokal
- **Pandas** - Data handling
- **JWT Auth** - Sistem login/register dengan role-based access
- **Alembic** - Database migration tool
- **Pydantic** - Data validation dan serialization

---

## 🧱 Struktur Proyek

```
app/
├── main.py # Entry point FastAPI dan semua endpoint
├── auth.py # Autentikasi dan token JWT
├── database.py # Koneksi database SQLite
├── models.py # ORM model User & Student
├── ml_model.py # Fungsi prediksi Random Forest
├── train_model.py # Training model dari dataset
├── test_model.py # Pengujian hasil prediksi
├── check_dataset.py # Pemeriksaan dataset mentah
├── visualize_model.py # Visualisasi evaluasi model
├── student_model.pkl # Model terlatih (binary)
├── tpq_dataset.csv # Dataset asli TPQ
```


---

## 🔐 Role dan Akses

| Role        | Akses                                    |
|-------------|------------------------------------------|
| `admin`     | CRUD data siswa, prediksi performa       |
| `orang_tua` | Lihat data anak & hasil prediksi         |

---

## 🔗 Dokumentasi API (Ringkasan Endpoint)

### 🔐 Auth
| Endpoint     | Method | Deskripsi                    |
|--------------|--------|------------------------------|
| `/register`  | POST   | Register user                |
| `/login`     | POST   | Login dan dapatkan JWT token |
| `/me`        | GET    | Lihat data user dari token   |

### 📚 Data Siswa
| Endpoint          | Method | Akses     | Deskripsi                   |
|-------------------|--------|-----------|-----------------------------|
| `/students`       | GET    | admin     | Lihat semua siswa           |
| `/students/{id}`  | GET    | admin/ortu| Lihat detail siswa          |
| `/students`       | POST   | admin     | Tambah siswa                |
| `/students/{id}`  | PUT    | admin     | Update data siswa           |
| `/students/{id}`  | DELETE | admin     | Hapus data siswa            |
| `/students/count` | GET    | admin     | Hitung jumlah total siswa   |

### 🎯 Kegiatan & Pengumuman
| Endpoint            | Method | Akses     | Deskripsi                     |
|---------------------|--------|-----------|-------------------------------|
| `/kegiatan`         | GET    | semua     | Lihat semua kegiatan          |
| `/kegiatan/{id}`    | GET    | semua     | Lihat detail kegiatan         |
| `/kegiatan`         | POST   | admin     | Tambah kegiatan               |
| `/kegiatan/{id}`    | PUT    | admin     | Update kegiatan               |
| `/kegiatan/{id}`    | DELETE | admin     | Hapus kegiatan                |
| `/pengumuman`       | GET    | semua     | Lihat semua pengumuman        |
| `/pengumuman/{id}`  | GET    | semua     | Lihat detail pengumuman       |
| `/pengumuman`       | POST   | admin     | Tambah pengumuman             |
| `/pengumuman/{id}`  | PUT    | admin     | Update pengumuman             |
| `/pengumuman/{id}`  | DELETE | admin     | Hapus pengumuman              |

### 🤖 Prediksi
| Endpoint     | Method | Akses     | Deskripsi                        |
|--------------|--------|-----------|----------------------------------|
| `/predict`   | POST   | semua     | Prediksi performa berdasarkan nilai |

---

## 🧠 Prediksi Model ML

Model menggunakan algoritma **Random Forest Classifier** berdasarkan 12 mata pelajaran siswa:

- Al-Quran/Iqro
- Hafalan Surat Pendek
- Hafalan Doa
- Hafalan Ayat Pilihan
- Bahasa Arab
- Bahasa Inggris
- Khat / Menulis
- Menggambar / Mewarnai
- Jasmani / Kesehatan
- Kreativitas / Keaktifan
- Ulumul Qur’an
- Kemampuan Berbahasa

### Parameter Model:
- **n_estimators:** 100 (jumlah pohon dalam forest)
- **max_depth:** 10 (kedalaman maksimum pohon)
- **min_samples_split:** 5 (minimum sampel untuk split)
- **min_samples_leaf:** 2 (minimum sampel di leaf node)
- **random_state:** 42 (untuk reproducibility)

### Output Prediksi:

- `BB` - Belum Berkembang
- `MB` - Mulai Berkembang
- `BSH` - Berkembang Sesuai Harapan
- `BSB` - Berkembang Sangat Baik

---

## 👥 Data Siswa

Sistem menyimpan data lengkap siswa meliputi:
- **Data Pribadi:** Nama, tanggal lahir, jenis kelamin, kelas
- **Kontak:** Nomor HP, nama orang tua
- **Akademik:** 12 nilai mata pelajaran (skala 0-100)
- **Hasil:** Rata-rata otomatis dan kategori prediksi

---

## 📊 Evaluasi Model

- **Akurasi model:** Ditampilkan melalui script `test_model.py`
- **Visualisasi:** Confusion matrix dan feature importance via `visualize_model.py`
- **Metrik evaluasi:** Precision, Recall, F1-Score untuk setiap kategori
- **Dataset:** 500 record siswa TPQ dengan 12 fitur nilai

---

## 🚀 Cara Menjalankan Lokal

### 1. Clone Repo & Masuk Folder
```bash
git clone <repo-url>
cd SALMA-ML-BE
```


### 2. Aktifkan Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

### 3. Install Dependency
```bash
pip install -r requirements.txt
```

### 4. Jalankan Model Trainer (sekali saja)
```bash
python app/train_model.py
```

### 5. Jalankan Database Migration
```bash
alembic upgrade head
```

### 6. Jalankan API Server
```bash
uvicorn app.main:app --reload
```

Akses via browser:
- **API Documentation:** http://127.0.0.1:8000/docs
- **Alternative Docs:** http://127.0.0.1:8000/redoc
- **Documentation HTML:** Buka file `documentation.html` di browser

---

## 📋 Testing API

### 1. Register Admin
```bash
curl -X POST "http://127.0.0.1:8000/register" \
     -H "Content-Type: application/json" \
     -d '{"username": "admin", "password": "admin123", "role": "admin"}'
```

### 2. Login dan Dapatkan Token
```bash
curl -X POST "http://127.0.0.1:8000/login" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "username=admin&password=admin123"
```

### 3. Test Prediksi
```bash
curl -X POST "http://127.0.0.1:8000/predict" \
     -H "Authorization: Bearer YOUR_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"al_quran_iqro": 85, "hafalan_surat_pendek": 80, ...}'
```

---

## 🔧 Database Migration

Jika ada perubahan model database:

```bash
# Generate migration baru
alembic revision --autogenerate -m "Deskripsi perubahan"

# Apply migration
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

---

## 📖 Dokumentasi

- **API Docs:** Swagger UI tersedia di `/docs`
- **Technical Docs:** File `documentation.html` dengan generator PDF
- **Model Info:** Script `test_model.py` untuk evaluasi model
- **Dataset Check:** Script `check_dataset.py` untuk validasi data

---

## 📝 Catatan

### ⚠️ Sebelum Production:
- Ubah `SECRET_KEY` di file `auth.py`
- Gunakan database PostgreSQL/MySQL untuk production
- Setup environment variables untuk konfigurasi
- Implementasi rate limiting dan CORS policy
- Backup model file `student_model.pkl`

### 🔒 Keamanan:
- Password di-hash menggunakan bcrypt
- JWT token dengan expiration time
- Role-based access control (admin/orang_tua)
- Input validation menggunakan Pydantic

### 📈 Performance:
- Model Random Forest dengan 100 estimators
- SQLite untuk development, PostgreSQL untuk production
- Async FastAPI untuk handling concurrent requests

---

## 📮 Kontak

**Dibuat oleh:** Yoki Jati Perkasa – Mahasiswa STMIK Mardira Indonesia  
**Proyek:** SALMA - Sistem Evaluasi Siswa TPQ Berbasis Machine Learning  
**Tahun:** 2025  
**Tech Stack:** Python, FastAPI, Scikit-Learn, SQLite, JWT  

---

## 🏆 Features Completed

- ✅ JWT Authentication dengan role-based access
- ✅ CRUD siswa dengan 12 parameter nilai + data pribadi lengkap
- ✅ Machine Learning prediction menggunakan Random Forest
- ✅ CRUD kegiatan dan pengumuman TPQ
- ✅ Database migration dengan Alembic
- ✅ API documentation dengan Swagger UI
- ✅ Model evaluation dan visualization tools
- ✅ Technical documentation dengan PDF generator
- ✅ Endpoint untuk statistik (jumlah siswa)
- ✅ Input validation dan error handling

**Status:** Production Ready 🚀