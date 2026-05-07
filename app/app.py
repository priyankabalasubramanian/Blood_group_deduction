"""
Flask Web App for Blood Group Prediction
- Users can upload an image and get predicted blood group
- Uses trained CNN model
"""
import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import numpy as np
import cv2
from tensorflow.keras.models import load_model

BLOOD_GROUPS = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
IMG_SIZE = (128, 128)
MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'models', 'blood_group_cnn.h5')
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

model = load_model(MODEL_PATH)

def predict_image(img_path):
    img = cv2.imread(img_path)
    img = cv2.resize(img, IMG_SIZE)
    img = img.astype(np.float32) / 255.0
    img = np.expand_dims(img, axis=0)
    pred = model.predict(img)
    idx = np.argmax(pred)
    return BLOOD_GROUPS[idx], float(np.max(pred))

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            label, conf = predict_image(filepath)
            return render_template('result.html', label=label, conf=conf, filename=filename)
    return render_template('index.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return redirect(url_for('static', filename='uploads/' + filename))

if __name__ == "__main__":
    app.run(debug=True)
