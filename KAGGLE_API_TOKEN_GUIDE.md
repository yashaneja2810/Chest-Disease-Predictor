# 🔑 Kaggle API Token Setup Guide

## You Have an API Token (Not kaggle.json)

Kaggle has updated their system! Instead of downloading a `kaggle.json` file, you now get an **API Token** string.

Your API Token: `KGAT_2967f7dc8630bc7987580c2cf613c4db`

---

## ✅ How to Use Your API Token in Google Colab

### Step 1: Open Your Notebook in Colab

Upload **`ChestX6_Training.ipynb`** to Google Colab (this is the updated notebook with 6 classes)

### Step 2: Run This Cell INSTEAD of Uploading kaggle.json

Replace the "Upload kaggle.json" cell with this code:

```python
# Setup Kaggle using API Token
import os
import json

# Your API token
api_token = "KGAT_2967f7dc8630bc7987580c2cf613c4db"

# Set environment variable
os.environ['KAGGLE_API_TOKEN'] = api_token

# Create kaggle directory
kaggle_dir = os.path.expanduser('~/.kaggle')
os.makedirs(kaggle_dir, exist_ok=True)

# Create kaggle.json file (for compatibility)
kaggle_json = {
    'username': 'your_username',  # Not critical with API token
    'key': api_token
}

with open(os.path.join(kaggle_dir, 'kaggle.json'), 'w') as f:
    json.dump(kaggle_json, f)

# Set proper permissions
!chmod 600 ~/.kaggle/kaggle.json

print("✅ Kaggle API configured successfully!")
```

### Step 3: Download the Dataset

Then run this cell:

```python
# Download the ChestX6 dataset
print("⬇️ Downloading dataset from Kaggle...")
!kaggle datasets download -d mohamedasak/chest-x-ray-6-classes-dataset

# Unzip
print("\n📦 Extracting dataset...")
!unzip -q chest-x-ray-6-classes-dataset.zip -d dataset

print("\n✅ Dataset ready!")
```

---

## 🎯 Quick Copy-Paste Solution

Just copy and paste these TWO cells at the beginning of your Colab notebook:

**Cell 1 - Setup Kaggle:**
```python
import os
import json

api_token = "KGAT_2967f7dc8630bc7987580c2cf613c4db"
os.environ['KAGGLE_API_TOKEN'] = api_token

kaggle_dir = os.path.expanduser('~/.kaggle')
os.makedirs(kaggle_dir, exist_ok=True)

kaggle_json = {'username': 'user', 'key': api_token}
with open(os.path.join(kaggle_dir, 'kaggle.json'), 'w') as f:
    json.dump(kaggle_json, f)

!chmod 600 ~/.kaggle/kaggle.json
print("✅ Kaggle configured!")
```

**Cell 2 - Download Dataset:**
```python
!kaggle datasets download -d mohamedasak/chest-x-ray-6-classes-dataset
!unzip -q chest-x-ray-6-classes-dataset.zip -d dataset
!ls -R dataset | head -30
print("✅ Dataset downloaded!")
```

---

## 📝 Which Notebook to Use?

**Use:** `ChestX6_Training.ipynb` (the newer one with 6 disease classes)

**Ignore:** `Chest_Xray_Training.ipynb` (old 2-class version)

The `ChestX6_Training.ipynb` is configured for:
- ✅ 6 disease classes (including COVID-19)
- ✅ 18,036 images
- ✅ Correct dataset link
- ✅ Better for your resume!

---

## ⚠️ Important Notes

1. **Don't share your API token publicly** - It's like a password
2. **The token in Colab is temporary** - It only exists during that session
3. **You can regenerate tokens** - If needed, go to Kaggle settings

---

## 🚀 Full Workflow

1. Open `ChestX6_Training.ipynb` in Google Colab
2. Enable GPU (Runtime → Change runtime type → GPU)
3. Run the API token setup cell (Cell 1 above)
4. Run the dataset download cell (Cell 2 above)
5. Continue with the rest of the notebook normally!

---

## ✅ That's It!

No need for `kaggle.json` file - your API token works perfectly! 🎉
