"""
Diagnose model predictions - check what the model is actually predicting
"""

import numpy as np
from tensorflow.keras.models import load_model
import sys

print("="*70)
print("🔍 MODEL DIAGNOSTIC TOOL")
print("="*70)

model_path = '../models/chest_xray_model.h5'

try:
    print(f"\n📦 Loading model from: {model_path}")
    model = load_model(model_path)
    print("✅ Model loaded!\n")
    
    print("📊 Model Architecture:")
    print(f"   Input shape: {model.input_shape}")
    print(f"   Output shape: {model.output_shape}")
    print(f"   Total parameters: {model.count_params():,}")
    
    # Get output layer
    output_layer = model.layers[-1]
    print(f"\n🎯 Output Layer:")
    print(f"   Type: {output_layer.__class__.__name__}")
    print(f"   Activation: {output_layer.activation.__name__}")
    print(f"   Units: {output_layer.units}")
    
    # Create a test input
    print("\n🧪 Testing with random input...")
    test_input = np.random.rand(1, 224, 224, 3).astype('float32')
    
    predictions = model.predict(test_input, verbose=0)
    print(f"\n📈 Prediction output:")
    print(f"   Shape: {predictions.shape}")
    print(f"   Values: {predictions[0]}")
    print(f"   Sum: {np.sum(predictions[0]):.6f}")
    print(f"   Max index: {np.argmax(predictions[0])}")
    print(f"   Max value: {np.max(predictions[0]):.6f}")
    
    # Expected class mapping based on training
    expected_classes = {
        0: 'Covid-19',
        1: 'Emphysema',
        2: 'Normal',
        3: 'Pneumonia-Bacterial',
        4: 'Pneumonia-Viral',
        5: 'Tuberculosis'
    }
    
    print(f"\n📋 Expected Class Mapping (alphabetical folder order):")
    for idx, name in expected_classes.items():
        prob = predictions[0][idx] * 100
        print(f"   {idx}: {name:20s} - {prob:6.2f}%")
    
    print("\n" + "="*70)
    print("✅ Model seems to be working correctly")
    print("="*70)
    
    # Check model file timestamp
    import os
    from datetime import datetime
    
    stat = os.stat(model_path)
    mod_time = datetime.fromtimestamp(stat.st_mtime)
    print(f"\n📅 Model file last modified: {mod_time}")
    print(f"💾 Model file size: {stat.st_size / (1024*1024):.1f} MB")
    
    # Check if this is the fine-tuned model
    if stat.st_size < 100 * 1024 * 1024:
        print("\n⚠️  WARNING: Model file seems small (< 100 MB)")
        print("   This might not be the fine-tuned model!")
    else:
        print(f"\n✅ Model file size looks correct (~{stat.st_size / (1024*1024):.0f} MB)")
    
    # Check if model was modified recently
    hours_old = (datetime.now() - mod_time).total_seconds() / 3600
    if hours_old > 24:
        print(f"\n⚠️  WARNING: Model is {hours_old/24:.1f} days old")
        print("   Did you download the fine-tuned model (best_model_finetuned.h5)?")
        print("   If not, this is the OLD model with potentially wrong predictions!")
    
except Exception as e:
    print(f"\n❌ Error: {str(e)}")
    import traceback
    traceback.print_exc()

print("\n" + "="*70)
