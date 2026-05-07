"""
Dataset Generation Script for Blood Group Classification
- Generates synthetic images for 8 blood groups
- Organizes images into train/val/test folders
- Each image is a colored label (for demo; replace with real images for production)
"""
import os
import cv2
import numpy as np
from sklearn.model_selection import train_test_split

BLOOD_GROUPS = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
SAMPLES_PER_CLASS = 100  # Adjust for more/less data
IMG_SIZE = (128, 128)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_DIR = os.path.join(BASE_DIR, '.')

np.random.seed(42)

# Create folders
def make_dirs():
    for split in ['train', 'val', 'test']:
        for group in BLOOD_GROUPS:
            path = os.path.join(DATASET_DIR, split, group)
            os.makedirs(path, exist_ok=True)

# Generate synthetic image (colored label)
def generate_image(label):
    img = np.ones((*IMG_SIZE, 3), dtype=np.uint8) * np.random.randint(100, 255)
    color = tuple(np.random.randint(0, 255, 3).tolist())
    cv2.putText(img, label, (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, color, 4, cv2.LINE_AA)
    return img

# Main dataset generation
def main():
    make_dirs()
    images, labels = [], []
    for group in BLOOD_GROUPS:
        for i in range(SAMPLES_PER_CLASS):
            img = generate_image(group)
            images.append(img)
            labels.append(group)
    images = np.array(images)
    labels = np.array(labels)

    # Split dataset
    X_train, X_temp, y_train, y_temp = train_test_split(images, labels, test_size=0.3, stratify=labels, random_state=42)
    X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, stratify=y_temp, random_state=42)

    # Save images
    def save_split(X, y, split):
        for idx, (img, label) in enumerate(zip(X, y)):
            path = os.path.join(DATASET_DIR, split, label, f"{label}_{idx}.png")
            cv2.imwrite(path, img)
    save_split(X_train, y_train, 'train')
    save_split(X_val, y_val, 'val')
    save_split(X_test, y_test, 'test')
    print("Dataset generated and split into train/val/test.")

if __name__ == "__main__":
    main()
