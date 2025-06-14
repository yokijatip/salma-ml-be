# file: test_model.py
import pickle
import numpy as np

def test_model():
    """
    Test model yang sudah di-train
    """
    try:
        # Load model
        with open("student_model.pkl", "rb") as f:
            model = pickle.load(f)
        
        print("Model loaded successfully!")
        print(f"Model type: {type(model)}")
        
        # Test dengan data sample
        test_cases = [
            # [Al_Quran_Iqro, Hafalan_Surat_Pendek, Hafalan_Doa, Hafalan_Ayat_Pilihan,
            #  Bahasa_Arab, Bahasa_Inggris, Khat_Menulis, Menggambar_Mewarnai,
            #  Jasmani_Kesehatan, Kreativitas_Keaktifan, Ulumul_Quran, Kemampuan_Berbahasa]
            
            # Test case 1: Nilai rendah (Expected: BB)
            [45, 50, 48, 52, 47, 49, 46, 51, 48, 50, 47, 49],
            
            # Test case 2: Nilai sedang (Expected: MB)
            [65, 62, 68, 64, 66, 63, 67, 65, 64, 66, 65, 63],
            
            # Test case 3: Nilai baik (Expected: BSH)
            [78, 75, 80, 77, 79, 76, 78, 82, 75, 80, 77, 79],
            
            # Test case 4: Nilai sangat baik (Expected: BSB)
            [92, 88, 95, 90, 93, 87, 91, 94, 89, 96, 90, 92],
            
            # Test case 5: Data dari contoh Anda
            [83, 77, 69, 75, 82, 74, 72, 85, 76, 82, 84, 82]
        ]
        
        expected_results = ["BB", "MB", "BSH", "BSB", "BSH"]
        
        print("\n=== TESTING MODEL ===")
        for i, test_data in enumerate(test_cases):
            # Prediksi
            input_data = np.array([test_data])
            prediction = model.predict(input_data)[0]
            
            # Hitung rata-rata manual untuk verifikasi
            avg = sum(test_data) / len(test_data)
            
            print(f"\nTest Case {i+1}:")
            print(f"Input: {test_data}")
            print(f"Average: {avg:.2f}")
            print(f"Expected: {expected_results[i]}")
            print(f"Predicted: {prediction}")
            print(f"Match: {'✓' if prediction == expected_results[i] else '✗'}")
        
        print("\n=== MODEL INFO ===")
        if hasattr(model, 'feature_importances_'):
            feature_names = [
                'Al_Quran_Iqro', 'Hafalan_Surat_Pendek', 'Hafalan_Doa', 'Hafalan_Ayat_Pilihan',
                'Bahasa_Arab', 'Bahasa_Inggris', 'Khat_Menulis', 'Menggambar_Mewarnai',
                'Jasmani_Kesehatan', 'Kreativitas_Keaktifan', 'Ulumul_Quran', 'Kemampuan_Berbahasa'
            ]
            
            importance_pairs = list(zip(feature_names, model.feature_importances_))
            importance_pairs.sort(key=lambda x: x[1], reverse=True)
            
            print("\nFeature Importance (Top 5):")
            for name, importance in importance_pairs[:5]:
                print(f"{name}: {importance:.4f}")
        
        return True
        
    except FileNotFoundError:
        print("Model file tidak ditemukan. Jalankan train_model.py terlebih dahulu.")
        return False
    except Exception as e:
        print(f"Error testing model: {str(e)}")
        return False

if __name__ == "__main__":
    test_model()