"""
Quick test to verify model class labels are correct
"""

from model import predictor
import json

print("="*60)
print("🧪 MODEL CLASS LABELS VERIFICATION")
print("="*60)

# Get model info
info = predictor.get_model_info()

if info['loaded']:
    print("\n✅ Model loaded successfully!\n")
    print("📋 Current Class Labels:")
    print(json.dumps(info['classes'], indent=2))
    
    print("\n📊 Expected Class Labels (from training):")
    expected_labels = {
        0: 'Covid-19',
        1: 'Emphysema',
        2: 'Normal',
        3: 'Pneumonia-Bacterial',
        4: 'Pneumonia-Viral',
        5: 'Tuberculosis'
    }
    print(json.dumps(expected_labels, indent=2))
    
    print("\n🔍 Verification:")
    if info['classes'] == expected_labels:
        print("✅ PASS: Class labels match training data!")
    else:
        print("❌ FAIL: Class labels DO NOT match!")
        print("\nDifferences:")
        for idx in range(6):
            current = info['classes'].get(idx, 'MISSING')
            expected = expected_labels.get(idx, 'MISSING')
            if current != expected:
                print(f"  Index {idx}: '{current}' != '{expected}'")
else:
    print("❌ Model not loaded!")

print("\n" + "="*60)
