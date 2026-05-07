import os
import cv2
import numpy as np
import time
from flask import Flask, request, jsonify, send_file, url_for
from flask_cors import CORS
from werkzeug.utils import secure_filename
import random

app = Flask(__name__, static_folder='../frontend', static_url_path='/')
CORS(app) # Enable CORS for all routes

UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = 'processed'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PROCESSED_FOLDER'] = PROCESSED_FOLDER

# Global variable to store current image path for demonstration purposes
current_image_path = None

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    global current_image_path
    if 'image' not in request.files:
        return jsonify({'error': 'No image part'}), 400
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        current_image_path = filepath
        # Return URL to access the uploaded image
        return jsonify({'message': 'File uploaded successfully', 'url': f'/image/uploads/{filename}'}), 200

@app.route('/image/<folder>/<filename>')
def get_image(folder, filename):
    if folder == 'uploads':
        return send_file(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    elif folder == 'processed':
        return send_file(os.path.join(app.config['PROCESSED_FOLDER'], filename))
    return jsonify({'error': 'Invalid folder'}), 400

@app.route('/process/color', methods=['POST'])
def process_color():
    global current_image_path
    if not current_image_path or not os.path.exists(current_image_path):
        return jsonify({'error': 'No image uploaded yet'}), 400
    
    img = cv2.imread(current_image_path)
    if img is None:
        return jsonify({'error': 'Failed to read image'}), 500

    # OpenCV uses BGR
    b, g, r = cv2.split(img)
    
    # Create zero arrays for other channels to show pure red and green planes
    zeros = np.zeros_like(b)
    red_plane = cv2.merge([zeros, zeros, r])
    green_plane = cv2.merge([zeros, g, zeros])
    
    red_filename = f"red_{os.path.basename(current_image_path)}"
    green_filename = f"green_{os.path.basename(current_image_path)}"
    
    red_path = os.path.join(app.config['PROCESSED_FOLDER'], red_filename)
    green_path = os.path.join(app.config['PROCESSED_FOLDER'], green_filename)
    
    cv2.imwrite(red_path, red_plane)
    cv2.imwrite(green_path, green_plane)
    
    return jsonify({
        'red_url': f'/image/processed/{red_filename}',
        'green_url': f'/image/processed/{green_filename}'
    })

@app.route('/process/threshold', methods=['POST'])
def process_threshold():
    global current_image_path
    if not current_image_path or not os.path.exists(current_image_path):
        return jsonify({'error': 'No image uploaded yet'}), 400
    
    img = cv2.imread(current_image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Apply Otsu's thresholding
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    
    thresh_filename = f"thresh_{os.path.basename(current_image_path)}"
    thresh_path = os.path.join(app.config['PROCESSED_FOLDER'], thresh_filename)
    cv2.imwrite(thresh_path, thresh)
    
    return jsonify({'url': f'/image/processed/{thresh_filename}'})

@app.route('/process/morphology', methods=['POST'])
def process_morphology():
    global current_image_path
    if not current_image_path or not os.path.exists(current_image_path):
        return jsonify({'error': 'No image uploaded yet'}), 400
    
    img = cv2.imread(current_image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    
    kernel = np.ones((5,5), np.uint8)
    # Opening (erosion followed by dilation) to remove noise
    morph = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
    # Closing to fill small holes
    morph = cv2.morphologyEx(morph, cv2.MORPH_CLOSE, kernel)
    
    morph_filename = f"morph_{os.path.basename(current_image_path)}"
    morph_path = os.path.join(app.config['PROCESSED_FOLDER'], morph_filename)
    cv2.imwrite(morph_path, morph)
    
    return jsonify({'url': f'/image/processed/{morph_filename}'})

@app.route('/process/hsi', methods=['POST'])
def process_hsi():
    global current_image_path
    if not current_image_path or not os.path.exists(current_image_path):
        return jsonify({'error': 'No image uploaded yet'}), 400
    
    img = cv2.imread(current_image_path)
    # OpenCV uses HSV, which is similar enough for demonstration
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    hsv_filename = f"hsi_{os.path.basename(current_image_path)}"
    hsv_path = os.path.join(app.config['PROCESSED_FOLDER'], hsv_filename)
    cv2.imwrite(hsv_path, hsv)
    
    return jsonify({'url': f'/image/processed/{hsv_filename}'})

@app.route('/detect', methods=['GET'])
def detect():
    global current_image_path
    start_time = time.time()
    
    if not current_image_path or not os.path.exists(current_image_path):
        return jsonify({'error': 'No image uploaded yet'}), 400
        
    img = cv2.imread(current_image_path, cv2.IMREAD_GRAYSCALE)
    
    # Calculate some simulated metrics based on the image
    mean_val = np.mean(img)
    rms_val = np.sqrt(np.mean(img**2))
    contrast_val = img.std()
    
    # Mock correlation
    correlation_val = random.uniform(0.7, 0.99)
    
    # Simple mocked detection logic for demo purposes based on mean intensity
    if mean_val < 100:
        blood_group = "A+"
    elif mean_val < 120:
        blood_group = "B+"
    elif mean_val < 140:
        blood_group = "AB+"
    else:
        blood_group = "O+"
        
    execution_time = time.time() - start_time
    
    return jsonify({
        'blood_group': blood_group,
        'parameters': {
            'Contrast': round(contrast_val, 2),
            'Mean': round(mean_val, 2),
            'RMS': round(rms_val, 2),
            'Correlation': round(correlation_val, 4),
            'Execution_Time': f"{round(execution_time * 1000, 2)} ms"
        }
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
