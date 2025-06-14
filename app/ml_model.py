# file: app/ml_model.py
import pickle
import numpy as np

# Load model sekali saja saat app berjalan
with open("app/student_model.pkl", "rb") as f:
    model = pickle.load(f)

def predict_performance(nilai_1, nilai_2, nilai_3, nilai_4):
    input_data = np.array([[nilai_1, nilai_2, nilai_3, nilai_4]])
    prediction = model.predict(input_data)
    return prediction[0]
