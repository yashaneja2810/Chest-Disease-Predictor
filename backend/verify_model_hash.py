"""
Verify model file identity and basic performance
"""
import hashlib
import os

model_path = '../models/chest_xray_model.h5'
fine_tuned_path = '../models/best_model_finetuned.h5'

def get_file_hash(filepath):
    """Calculate MD5 hash of file"""
    if not os.path.exists(filepath):
        return None
    
    md5_hash = hashlib.md5()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            md5_hash.update(chunk)
    return md5_hash.hexdigest()

print("="*70)
print("MODEL FILE VERIFICATION")
print("="*70)

# Check both files
files_to_check = [
    ('Current model', model_path),
    ('Fine-tuned backup', fine_tuned_path)
]

hashes = {}
for name, path in files_to_check:
    abs_path = os.path.abspath(path)
    if os.path.exists(abs_path):
        size_mb = os.path.getsize(abs_path) / (1024**2)
        file_hash = get_file_hash(abs_path)
        hashes[name] = file_hash
        
        print(f"\n{name}:")
        print(f"  Path: {abs_path}")
        print(f"  Size: {size_mb:.1f} MB")
        print(f"  MD5:  {file_hash}")
    else:
        print(f"\n{name}: NOT FOUND")
        print(f"  Expected at: {abs_path}")

print("\n" + "="*70)

# Compare
if len(hashes) == 2:
    if hashes['Current model'] == hashes['Fine-tuned backup']:
        print("⚠️  BOTH FILES ARE IDENTICAL!")
        print("You need to download the REAL fine-tuned model from Colab")
    else:
        print("✅ Files are different")
else:
    print("⚠️  Could not compare - missing files")

print("="*70)
print("\n📋 Expected MD5 from your training:")
print("   (Check your Colab notebook output after training)")
print("   If you saved with model.save(), Colab should show file size")
print("\n   Current MD5: " + hashes.get('Current model', 'N/A'))
print("="*70)
