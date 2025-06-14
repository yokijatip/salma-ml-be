# file: app/train_model.py
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import pickle

def train_model_with_csv(csv_file_path):
    """
    Train model menggunakan dataset CSV
    """
    try:
        # Load dataset
        print("Loading dataset...")
        df = pd.read_csv(csv_file_path)
        print(f"Dataset loaded: {len(df)} rows")
        
        # Cek kolom yang diperlukan (sesuaikan dengan dataset Anda)
        required_columns = [
            'Al_Quran_Iqro', 'Hafalan_Surat_Pendek', 'Hafalan_Doa', 'Hafalan_Ayat_Pilihan',
            'Bahasa_Arab', 'Bahasa_Inggris', 'Khat_Menulis', 'Menggambar_Mewarnai',
            'Jasmani_Kesehatan', 'Kreativitas_Keaktifan', 'Ulumul_Quran', 'Kemampuan_Berbahasa',
            'Kategori'
        ]
        
        # Pastikan semua kolom ada
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            print(f"Missing columns: {missing_columns}")
            print(f"Available columns: {list(df.columns)}")
            return False
        
        # Prepare features dan target
        X = df[[
            'Al_Quran_Iqro', 'Hafalan_Surat_Pendek', 'Hafalan_Doa', 'Hafalan_Ayat_Pilihan',
            'Bahasa_Arab', 'Bahasa_Inggris', 'Khat_Menulis', 'Menggambar_Mewarnai',
            'Jasmani_Kesehatan', 'Kreativitas_Keaktifan', 'Ulumul_Quran', 'Kemampuan_Berbahasa'
        ]]
        y = df['Kategori']
        
        print(f"Features shape: {X.shape}")
        print(f"Target distribution:\n{y.value_counts()}")
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
        
        # Training model
        print("Training model...")
        model = RandomForestClassifier(
            n_estimators=100,
            random_state=42,
            max_depth=10,
            min_samples_split=5,
            min_samples_leaf=2
        )
        model.fit(X_train, y_train)
        
        # Evaluasi model
        train_accuracy = model.score(X_train, y_train)
        test_accuracy = model.score(X_test, y_test)
        
        print(f"Training Accuracy: {train_accuracy:.4f}")
        print(f"Testing Accuracy: {test_accuracy:.4f}")
        
        # Prediksi untuk classification report
        y_pred = model.predict(X_test)
        print("\nClassification Report:")
        print(classification_report(y_test, y_pred))
        
        # Simpan model
        with open("app/student_model.pkl", "wb") as f:
            pickle.dump(model, f)
        
        print("Model berhasil disimpan ke app/student_model.pkl")
        return True
        
    except Exception as e:
        print(f"Error training model: {str(e)}")
        return False

def create_sample_data():
    """
    Buat sample data jika tidak ada CSV
    """
    print("Creating sample data...")
    
    # Data sample yang lebih realistis
    import random
    
    data = []
    for i in range(1000):
        # Generate nilai dengan pola tertentu
        base_performance = random.choice(['low', 'medium', 'high', 'excellent'])
        
        if base_performance == 'low':
            values = [random.randint(40, 59) for _ in range(12)]
            kategori = 'BB'
        elif base_performance == 'medium':
            values = [random.randint(60, 69) for _ in range(12)]
            kategori = 'MB'
        elif base_performance == 'high':
            values = [random.randint(70, 84) for _ in range(12)]
            kategori = 'BSH'
        else:  # excellent
            values = [random.randint(85, 100) for _ in range(12)]
            kategori = 'BSB'
        
        # Tambah sedikit variasi
        values = [max(0, min(100, val + random.randint(-5, 5))) for val in values]
        
        row = {
            'ID': i+1,
            'Nama': f'Siswa_{i+1}',
            'Kelas': random.choice(['I.1', 'I.2', 'I.3', 'I.4', 'I.5']),
            'Al_Quran_Iqro': values[0],
            'Hafalan_Surat_Pendek': values[1],
            'Hafalan_Doa': values[2],
            'Hafalan_Ayat_Pilihan': values[3],
            'Bahasa_Arab': values[4],
            'Bahasa_Inggris': values[5],
            'Khat_Menulis': values[6],
            'Menggambar_Mewarnai': values[7],
            'Jasmani_Kesehatan': values[8],
            'Kreativitas_Keaktifan': values[9],
            'Ulumul_Quran': values[10],
            'Kemampuan_Berbahasa': values[11],
            'Rata_Rata': sum(values) / len(values),
            'Kategori': kategori
        }
        data.append(row)
    
    df = pd.DataFrame(data)
    df.to_csv('sample_dataset.csv', index=False)
    print("Sample dataset saved to sample_dataset.csv")
    return df

if __name__ == "__main__":
    # Path ke dataset CSV Anda
    # csv_path = "tpq_dataset.csv"  # Jika di root project
    csv_path = "app/tpq_dataset.csv"  # Jika di folder app/
    
    # Coba load dataset CSV Anda
    try:
        success = train_model_with_csv(csv_path)
        if not success:
            print("Gagal load dataset, membuat sample data...")
            df = create_sample_data()
            train_model_with_csv('sample_dataset.csv')
    except FileNotFoundError:
        print(f"File {csv_path} tidak ditemukan!")
        print("Pastikan file CSV sudah diletakkan di lokasi yang benar.")
        print("Atau buat sample data dengan uncomment baris di bawah:")
        # df = create_sample_data()
        # train_model_with_csv('sample_dataset.csv')