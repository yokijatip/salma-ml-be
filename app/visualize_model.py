import joblib
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
from sklearn.tree import plot_tree
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import numpy as np
import os
import seaborn as sns

os.makedirs("visualizations", exist_ok=True)

# lanjutkan proses visualisasi...
plt.savefig("visualizations/confusion_matrix.png")

# Pastikan folder 'visualizations/' ada
os.makedirs("visualizations", exist_ok=True)


# === Load model dan data ===
model = joblib.load("app/student_model.pkl")
data = pd.read_csv("app/tpq_dataset.csv")  # Dataset asli
X = data.drop(columns=["Kategori", "ID", "Nama", "Kelas", "Rata_Rata"])# hapus kolom non-fitur
y = data["Kategori"]

# === Confusion Matrix ===
y_pred = model.predict(X)
cm = confusion_matrix(y, y_pred, labels=model.classes_)

disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=model.classes_)
disp.plot(cmap="Blues", values_format="d")
plt.title("Confusion Matrix")
plt.savefig("visualizations/confusion_matrix.png")
plt.close()

# === Feature Importance ===
importances = model.feature_importances_
feature_names = X.columns

plt.figure(figsize=(10, 6))
sns.barplot(x=importances, y=feature_names)
plt.title("Feature Importances")
plt.xlabel("Importance")
plt.ylabel("Features")
plt.tight_layout()
plt.savefig("visualizations/feature_importance.png")
plt.close()

# === Visualisasi Salah Satu Pohon ===
estimator = model.estimators_[0]  # Ambil 1 pohon dari random forest
plt.figure(figsize=(20, 10))
plot_tree(estimator, feature_names=feature_names, class_names=model.classes_, filled=True)
plt.title("Example Decision Tree")
plt.savefig("visualizations/sample_tree.png")
plt.close()
