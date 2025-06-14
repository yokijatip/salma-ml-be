# evaluate_model.py
import pandas as pd
import pickle
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# 1. Load data dummy / dataset asli
data = {
    'nilai_1': [80, 60, 40, 90, 65, 45, 88],
    'nilai_2': [85, 65, 50, 92, 60, 42, 90],
    'nilai_3': [78, 70, 55, 95, 64, 40, 87],
    'nilai_4': [82, 62, 45, 96, 61, 44, 89],
    'label': ['BSH', 'MB', 'BB', 'BSB', 'MB', 'BB', 'BSB']
}
df = pd.DataFrame(data)
X = df[['nilai_1', 'nilai_2', 'nilai_3', 'nilai_4']]
y_true = df['label']

# 2. Load model
with open("student_model.pkl", "rb") as f:
    model = pickle.load(f)

# 3. Prediksi
y_pred = model.predict(X)

# 4. Evaluasi
print("=== Akurasi ===")
print(f"{accuracy_score(y_true, y_pred):.2f}")

print("\n=== Classification Report ===")
print(classification_report(y_true, y_pred))

# 5. Confusion Matrix Visual
cm = confusion_matrix(y_true, y_pred, labels=["BB", "MB", "BSH", "BSB"])
plt.figure(figsize=(6, 5))
sns.heatmap(cm, annot=True, fmt='d', xticklabels=["BB", "MB", "BSH", "BSB"], yticklabels=["BB", "MB", "BSH", "BSB"])
plt.title("Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.tight_layout()
plt.savefig("confusion_matrix.png")  # Simpan hasil ke file
plt.show()
