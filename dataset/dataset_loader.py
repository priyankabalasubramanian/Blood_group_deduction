"""
Dataset Loader Script
- Loads images and labels from dataset folders
- Prepares data for model training
"""
import os
import cv2
import numpy as np
from tensorflow.keras.utils import to_categorical

BLOOD_GROUPS = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
IMG_SIZE = (128, 128)

# Map blood group to index
group2idx = {bg: i for i, bg in enumerate(BLOOD_GROUPS)}

def load_dataset(base_dir, split):
    X, y = [], []
    split_dir = os.path.join(base_dir, split)
    for group in BLOOD_GROUPS:
        group_dir = os.path.join(split_dir, group)
        for fname in os.listdir(group_dir):
            img_path = os.path.join(group_dir, fname)
            img = cv2.imread(img_path)
            img = cv2.resize(img, IMG_SIZE)
            X.append(img)
            y.append(group2idx[group])
    X = np.array(X, dtype=np.float32) / 255.0
    y = to_categorical(y, num_classes=len(BLOOD_GROUPS))
    return X, y

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    for split in ['train', 'val', 'test']:
        X, y = load_dataset(base_dir, split)
        print(f"Loaded {split}: X={X.shape}, y={y.shape}")
