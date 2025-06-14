# file: train_model.py
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import pickle

# Buat data dummy
data = {
    'nilai_1': [80, 60, 40, 90],
    'nilai_2': [85, 65, 50, 92],
    'nilai_3': [78, 70, 55, 95],
    'nilai_4': [82, 62, 45, 96],
    'label': ['BSH', 'MB', 'BB', 'BSB']
}
df = pd.DataFrame(data)

# Training
X = df[['nilai_1', 'nilai_2', 'nilai_3', 'nilai_4']]
y = df['label']
model = RandomForestClassifier()
model.fit(X, y)

# Simpan model
with open("student_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("Model berhasil disimpan.")