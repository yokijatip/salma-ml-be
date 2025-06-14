# file: check_dataset.py
import pandas as pd

def check_dataset(csv_path):
    """
    Cek struktur dan isi dataset
    """
    try:
        df = pd.read_csv(csv_path)
        
        print(f"Dataset loaded successfully!")
        print(f"Shape: {df.shape}")
        print(f"\nColumns: {list(df.columns)}")
        
        print(f"\nFirst 5 rows:")
        print(df.head())
        
        print(f"\nDataset info:")
        print(df.info())
        
        if 'Kategori' in df.columns:
            print(f"\nKategori distribution:")
            print(df['Kategori'].value_counts())
        
        # Cek missing values
        missing = df.isnull().sum()
        if missing.sum() > 0:
            print(f"\nMissing values:")
            print(missing[missing > 0])
        else:
            print(f"\nNo missing values found!")
        
        return True
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

if __name__ == "__main__":
    csv_path = "app/tpq_dataset.csv"  # Sesuaikan dengan lokasi file
    check_dataset(csv_path)