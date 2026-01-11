# Models Folder

This folder will contain your trained deep learning model.

## Required File

**`chest_xray_model.h5`** - The trained TensorFlow/Keras model

## How to Get the Model

1. Open `model_training/Chest_Xray_Training.ipynb` in Google Colab
2. Follow the instructions to train the model (takes 30-60 minutes)
3. Download the generated `chest_xray_model.h5` file
4. Place it in this folder

## Model Details

- **Architecture:** ResNet50 (Transfer Learning)
- **Input Size:** 224x224x3 (RGB images)
- **Output:** 2 classes (NORMAL, PNEUMONIA)
- **File Size:** ~90-100 MB
- **Format:** HDF5 (.h5)

## Alternative: Pre-trained Model

If you want to skip training, you can:
1. Request a pre-trained model from the project maintainer
2. Or train your own following the Colab notebook

## Important Notes

⚠️ **Do NOT commit the model file to Git** - it's too large!
- The `.gitignore` file already excludes `*.h5` files
- Download/train the model separately for each deployment

✅ **Verify the model is loaded**
- Run `python backend/model.py` to test model loading
- The backend will show "Model loaded successfully" when you start the server
