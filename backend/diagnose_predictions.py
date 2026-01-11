"""
Diagnose model predictions - check if model is biased
"""
import numpy as np
import tensorflow as tf
from tensorflow import keras
import sys

print("Loading model...")
model = keras.models.load_model('../models/chest_xray_model.h5')

class_labels = ['Covid-19', 'Emphysema', 'Normal', 'Pneumonia-Bacterial', 'Pneumonia-Viral', 'Tuberculosis']

print(f"✅ Model loaded: {model.input_shape} -> {model.output_shape}\n")

# Test 10 random images
print("="*70)
print("TESTING WITH 10 RANDOM NOISE IMAGES")
print("="*70)

class_counts = {label: 0 for label in class_labels}

for i in range(10):
    random_img = np.random.rand(1, 224, 224, 3).astype('float32')
    pred = model.predict(random_img, verbose=0)
    predicted_idx = np.argmax(pred[0])
    predicted_class = class_labels[predicted_idx]
    confidence = pred[0][predicted_idx] * 100
    
    class_counts[predicted_class] += 1
    
    print(f"Test {i+1}: {predicted_class:25s} ({confidence:5.2f}%)")
    if i == 0:
        print(f"        Raw output: {pred[0]}")

print("\n" + "="*70)
print("SUMMARY - Predictions on random noise:")
print("="*70)
for label, count in class_counts.items():
    print(f"{label:25s}: {count}/10 times")

if class_counts['Emphysema'] >= 8:
    print("\n⚠️  CRITICAL: Model is BIASED toward Emphysema!")
    print("This is NOT a fine-tuned model - it's either:")
    print("  1. Pre-trained (not fine-tuned)")
    print("  2. Poorly trained")
    print("  3. Corrupted weights")
elif class_counts['Normal'] >= 8:
    print("\n⚠️  Model is BIASED toward Normal!")
    
print("\n" + "="*70)
print("Next: Open http://localhost:5000/api/debug to see class labels")
print("="*70)
