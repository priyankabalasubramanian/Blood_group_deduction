"""
Prediction Script for Blood Group Classification
- Loads trained model
- Predicts blood group for a given image
- Usage: python testing/predict.py path/to/image.png
"""
import sys
import os
import numpy as np
import cv2
from tensorflow.keras.models import load_model

BLOOD_GROUPS = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
IMG_SIZE = (128, 128)
MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'models', 'blood_group_cnn.h5')

def predict_image(img_path):
    model = load_model(MODEL_PATH)
    img = cv2.imread(img_path)
    img = cv2.resize(img, IMG_SIZE)
    img = img.astype(np.float32) / 255.0
    img = np.expand_dims(img, axis=0)
    pred = model.predict(img)
    idx = np.argmax(pred)
    return BLOOD_GROUPS[idx], float(np.max(pred))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python testing/predict.py path/to/image.png")
        sys.exit(1)
    img_path = sys.argv[1]
    label, conf = predict_image(img_path)
    print(f"Predicted: {label} (Confidence: {conf:.2f})")
