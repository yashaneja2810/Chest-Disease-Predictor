"""
Test model predictions with detailed output
"""
import numpy as np
from PIL import Image
import tensorflow as tf
from tensorflow import keras

# Load model
print("Loading model...")
model = keras.models.load_model('../models/chest_xray_model.h5')

# Class labels (alphabetical order)
class_labels = {
    0: 'Covid-19',
    1: 'Emphysema', 
    2: 'Normal',
    3: 'Pneumonia-Bacterial',
    4: 'Pneumonia-Viral',
    5: 'Tuberculosis'
}

print(f"\n✅ Model loaded")
print(f"Input shape: {model.input_shape}")
print(f"Output shape: {model.output_shape}")

# Test with a simple pattern
print("\n" + "="*60)
print("TESTING WITH RANDOM NOISE")
print("="*60)

# Create random noise image
random_image = np.random.rand(1, 224, 224, 3).astype('float32')
predictions = model.predict(random_image, verbose=0)

print(f"\nRaw predictions array:\n{predictions[0]}")
print(f"\nSum of probabilities: {predictions[0].sum():.6f}")

print("\nAll class probabilities:")
for idx, label in class_labels.items():
    prob = predictions[0][idx] * 100
    print(f"  {idx}: {label:25s} -> {prob:6.2f}%")

predicted_class_idx = np.argmax(predictions[0])
predicted_class = class_labels[predicted_class_idx]
confidence = predictions[0][predicted_class_idx] * 100

print(f"\n🎯 Predicted: {predicted_class} ({confidence:.2f}%)")

# Now ask for user image
print("\n" + "="*60)
print("MANUAL IMAGE TEST")
print("="*60)
print("\nPaste the full path to your test X-ray image:")
print("(e.g., C:\\Users\\YourName\\Downloads\\tb_xray.jpg)")
