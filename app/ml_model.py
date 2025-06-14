# file: app/ml_model.py
import pickle
import numpy as np
import pandas as pd
import os

def load_model():
    """Load model dari berbagai kemungkinan lokasi"""
    model_paths = [
        "student_model.pkl",  # Root directory
        "app/student_model.pkl",  # App directory  
        os.path.join(os.path.dirname(__file__), "student_model.pkl"),  # Same directory as this file
        os.path.join(os.path.dirname(__file__), "..", "student_model.pkl"),  # Parent directory
    ]
    
    for path in model_paths:
        try:
            if os.path.exists(path):
                with open(path, "rb") as f:
                    model = pickle.load(f)
                print(f"Model loaded from: {path}")
                return model
        except Exception as e:
            print(f"Failed to load model from {path}: {e}")
            continue
    
    raise FileNotFoundError(
        "Model file tidak ditemukan! Pastikan sudah menjalankan train_model.py terlebih dahulu."
    )

# Load model sekali saja saat app berjalan
try:
    model = load_model()
except FileNotFoundError as e:
    print(f"WARNING: {e}")
    model = None

# Feature names yang sama dengan yang digunakan saat training
FEATURE_NAMES = [
    'Al_Quran_Iqro', 'Hafalan_Surat_Pendek', 'Hafalan_Doa', 'Hafalan_Ayat_Pilihan',
    'Bahasa_Arab', 'Bahasa_Inggris', 'Khat_Menulis', 'Menggambar_Mewarnai',
    'Jasmani_Kesehatan', 'Kreativitas_Keaktifan', 'Ulumul_Quran', 'Kemampuan_Berbahasa'
]

def predict_performance(al_quran_iqro, hafalan_surat_pendek, hafalan_doa, hafalan_ayat_pilihan, 
                       bahasa_arab, bahasa_inggris, khat_menulis, menggambar_mewarnai, 
                       jasmani_kesehatan, kreativitas_keaktifan, ulumul_quran, kemampuan_berbahasa):
    """
    Prediksi performa siswa berdasarkan 12 mata pelajaran
    """
    if model is None:
        raise Exception("Model tidak tersedia. Jalankan train_model.py terlebih dahulu.")
    
    # Buat DataFrame dengan nama kolom yang sama seperti saat training
    input_data = pd.DataFrame([{
        'Al_Quran_Iqro': al_quran_iqro,
        'Hafalan_Surat_Pendek': hafalan_surat_pendek,
        'Hafalan_Doa': hafalan_doa,
        'Hafalan_Ayat_Pilihan': hafalan_ayat_pilihan,
        'Bahasa_Arab': bahasa_arab,
        'Bahasa_Inggris': bahasa_inggris,
        'Khat_Menulis': khat_menulis,
        'Menggambar_Mewarnai': menggambar_mewarnai,
        'Jasmani_Kesehatan': jasmani_kesehatan,
        'Kreativitas_Keaktifan': kreativitas_keaktifan,
        'Ulumul_Quran': ulumul_quran,
        'Kemampuan_Berbahasa': kemampuan_berbahasa
    }])
    
    # Pastikan urutan kolom sama dengan saat training
    input_data = input_data[FEATURE_NAMES]
    
    prediction = model.predict(input_data)
    return prediction[0]