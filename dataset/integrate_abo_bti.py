"""
Integrate ABO-BTI Dataset: Organize images into train/val/test folders for model training.
- Reads images from raw/images/
- Maps folder names to blood group labels
- Splits into train (70%), val (15%), test (15%)
- Saves to dataset/train, dataset/val, dataset/test
"""
import os
import shutil
import numpy as np
from sklearn.model_selection import train_test_split

# Map folder names to standard blood group labels
FOLDER2LABEL = {
    'A positive': 'A+',
    'A negative': 'A-',
    'B positive': 'B+',
    'B negative': 'B-',
    'AB positive': 'AB+',
    'AB negative': 'AB-',
    'O positive': 'O+',
    'O negative': 'O-'
}

RAW_IMG_DIR = os.path.join(os.path.dirname(__file__), 'raw', 'images')
DATASET_DIR = os.path.dirname(__file__)
SPLITS = {'train': 0.7, 'val': 0.15, 'test': 0.15}

np.random.seed(42)

def make_dirs():
    for split in SPLITS:
        for label in FOLDER2LABEL.values():
            path = os.path.join(DATASET_DIR, split, label)
            os.makedirs(path, exist_ok=True)

def collect_images():
    data = []
    for folder, label in FOLDER2LABEL.items():
        folder_path = os.path.join(RAW_IMG_DIR, folder)
        for fname in os.listdir(folder_path):
            if fname.lower().endswith('.jpg'):
                data.append((os.path.join(folder_path, fname), label))
    return np.array(data)

def split_and_copy(data):
    X = data[:,0]
    y = data[:,1]
    X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.3, stratify=y, random_state=42)
    X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, stratify=y_temp, random_state=42)
    splits = [('train', X_train, y_train), ('val', X_val, y_val), ('test', X_test, y_test)]
    for split, Xs, ys in splits:
        for src, label in zip(Xs, ys):
            dst = os.path.join(DATASET_DIR, split, label, os.path.basename(src))
            shutil.copy2(src, dst)

def main():
    make_dirs()
    data = collect_images()
    split_and_copy(data)
    print('ABO-BTI dataset integrated and split into train/val/test.')

if __name__ == "__main__":
    main()
