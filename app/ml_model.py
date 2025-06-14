# file: app/ml_model.py
import pickle
import numpy as np

# Load model sekali saja saat app berjalan
with open("app/student_model.pkl", "rb") as f:
    model = pickle.load(f)

def predict_performance(al_quran_iqro, hafalan_surat_pendek, hafalan_doa, hafalan_ayat_pilihan, 
                       bahasa_arab, bahasa_inggris, khat_menulis, menggambar_mewarnai, 
                       jasmani_kesehatan, kreativitas_keaktifan, ulumul_quran, kemampuan_berbahasa):
    """
    Prediksi performa siswa berdasarkan 12 mata pelajaran
    """
    input_data = np.array([[
        al_quran_iqro, hafalan_surat_pendek, hafalan_doa, hafalan_ayat_pilihan,
        bahasa_arab, bahasa_inggris, khat_menulis, menggambar_mewarnai,
        jasmani_kesehatan, kreativitas_keaktifan, ulumul_quran, kemampuan_berbahasa
    ]])
    
    prediction = model.predict(input_data)
    return prediction[0]