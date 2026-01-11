"""
Check if the model needs different preprocessing (e.g., ImageNet normalization)
"""
import numpy as np
from PIL import Image
import tensorflow as tf
from tensorflow import keras

print("Testing different preprocessing methods...\n")

# Load model
model = keras.models.load_model('../models/chest_xray_model.h5')

# Create a sample image (simulating X-ray - mostly dark with some bright areas)
sample_img = np.zeros((224, 224, 3), dtype=np.uint8)
sample_img[50:150, 50:150] = 200  # Bright square (simulating lung area)

print("Sample image stats:")
print(f"  Min: {sample_img.min()}, Max: {sample_img.max()}")
print(f"  Mean: {sample_img.mean():.2f}\n")

# Method 1: Simple normalization (0-1) - CURRENT METHOD
img1 = sample_img.astype('float32') / 255.0
img1_batch = np.expand_dims(img1, axis=0)
pred1 = model.predict(img1_batch, verbose=0)

print("Method 1: Simple normalization (current)")
print(f"  Preprocessed range: [{img1.min():.3f}, {img1.max():.3f}]")
print(f"  Prediction shape: {pred1.shape}")
print(f"  Max probability: {pred1.max():.4f}")
print(f"  Predicted class: {np.argmax(pred1[0])}\n")

# Method 2: ImageNet preprocessing (mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
img2 = sample_img.astype('float32') / 255.0
imagenet_mean = np.array([0.485, 0.456, 0.406])
imagenet_std = np.array([0.229, 0.224, 0.225])
img2 = (img2 - imagenet_mean) / imagenet_std
img2_batch = np.expand_dims(img2, axis=0)
pred2 = model.predict(img2_batch, verbose=0)

print("Method 2: ImageNet normalization")
print(f"  Preprocessed range: [{img2.min():.3f}, {img2.max():.3f}]")
print(f"  Prediction shape: {pred2.shape}")
print(f"  Max probability: {pred2.max():.4f}")
print(f"  Predicted class: {np.argmax(pred2[0])}\n")

# Method 3: Scale to [-1, 1]
img3 = sample_img.astype('float32') / 127.5 - 1.0
img3_batch = np.expand_dims(img3, axis=0)
pred3 = model.predict(img3_batch, verbose=0)

print("Method 3: Scale to [-1, 1]")
print(f"  Preprocessed range: [{img3.min():.3f}, {img3.max():.3f}]")
print(f"  Prediction shape: {pred3.shape}")
print(f"  Max probability: {pred3.max():.4f}")
print(f"  Predicted class: {np.argmax(pred3[0])}\n")

print("="*70)
print("❓ QUESTION: Which preprocessing did you use in Colab training?")
print("="*70)
print("\nCheck your Colab notebook for lines like:")
print("  • preprocess_input from tensorflow.keras.applications.resnet50")
print("  • ImageDataGenerator(rescale=1./255)")
print("  • ImageDataGenerator(preprocessing_function=...)")
print("  • Manual normalization with mean/std")
print("\nIf you used ResNet50 preprocess_input, that's ImageNet normalization!")
print("="*70)
