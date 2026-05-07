# Automated Blood Group Detection (AI & ML)

This project provides an end-to-end solution for automated blood group classification using deep learning (CNN) and a Flask web application. It includes dataset generation, model training, evaluation, and a modern web UI for predictions.

## Features
- Synthetic and sample dataset generation for 8 blood groups
- CNN model with TensorFlow/Keras
- Data preprocessing and augmentation
- Training, validation, and testing splits
- Evaluation metrics: Accuracy, Precision, Recall, F1-score
- Confusion matrix and training graphs
- Flask web app for image upload and prediction
- Modern HTML/CSS UI
- Beginner-friendly structure and code

## Project Structure
```
dataset/        # Blood group images (organized by label)
models/         # Saved models (.h5)
training/       # Training scripts and logs
results/        # Evaluation results, graphs
app/            # Flask web app
```

## Setup Instructions
1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
2. **Generate dataset:**
   ```bash
   python dataset/generate_dataset.py
   ```
3. **Train the model:**
   ```bash
   python training/train.py
   ```
4. **Run the web app:**
   ```bash
   python app/app.py
   ```

## References
- ABO-BTI Dataset
- Kaggle Fingerprint Blood Group Dataset
- Research: Automated blood group identification using ML/DL (98.5% accuracy)

---

For more details, see code comments and documentation in each folder.