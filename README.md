# SALMA-ML-BE

**Sistem Backend Machine Learning untuk Evaluasi Performa Siswa TPQ menggunakan FastAPI dan Random Forest**

---

## 📌 Deskripsi

Proyek ini adalah backend berbasis Python (FastAPI) yang memanfaatkan algoritma Machine Learning (Random Forest) untuk memprediksi performa siswa pada lembaga pendidikan seperti TPQ. Sistem ini memungkinkan:

- Admin mengelola data siswa
- Orang tua melihat hasil evaluasi anaknya
- Prediksi performa siswa otomatis berdasarkan 12 parameter nilai
- Evaluasi performa model (akurasi, confusion matrix, dll)

---

## ⚙️ Teknologi yang Digunakan

- **FastAPI** - Web framework Python
- **Scikit-Learn** - Machine Learning (Random Forest)
- **SQLite + SQLAlchemy** - Database lokal
- **Pandas** - Data handling
- **Matplotlib / Seaborn** - Visualisasi evaluasi model
- **JWT Auth** - Sistem login/register dengan role-based access

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
├── student_model.pkl # Model terlatih (binary)
├── sample_dataset.csv # Dataset dummy hasil generate
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

### 🤖 Prediksi
| Endpoint     | Method | Akses     | Deskripsi                        |
|--------------|--------|-----------|----------------------------------|
| `/predict`   | POST   | semua     | Prediksi performa berdasarkan nilai |

---

## 🧠 Prediksi Model ML

Model menggunakan algoritma **Random Forest Classifier** berdasarkan 12 nilai siswa:

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

### Output Prediksi:

- `BB` - Belum Berkembang
- `MB` - Mulai Berkembang
- `BSH` - Berkembang Sesuai Harapan
- `BSB` - Berkembang Sangat Baik

---

## 📊 Evaluasi Model

- Akurasi model ditampilkan melalui script `test_model.py` & `evaluate_model.py`
- Visualisasi confusion matrix tersimpan di `confusion_matrix.png`
- Dapat ditampilkan ke admin melalui dashboard/endpoint terpisah

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
### 5. Jalnkan API Server
```bash
uvicorn app.main:app --reload
```

Akses via browser:
Swagger UI: http://127.0.0.1:8000/docs#/

---

## 📝 Catatan
- Ubah SECRET_KEY di file auth.py sebelum production
- Jangan upload student_model.pkl besar ke GitHub
- Tambahkan .env file jika nanti butuh config dinamis

---

## 📮 Kontak
| Dibuat oleh Yoki Jati Perkasa – Mahasiswa STMIK Mardira Indonesia
| Proyek JOKI: Evaluasi Siswa TPQ Berbasis Machine Learning
| Tahun 2025