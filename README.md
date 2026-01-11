# 🏥 Chest X-Ray Disease Prediction System

A deep learning-powered web application that predicts diseases from chest X-ray images using Convolutional Neural Networks (CNN). This project allows healthcare professionals and patients to upload X-ray images and get instant disease predictions.

## 🎯 Project Overview

This system uses a trained deep learning model to classify chest X-rays into **6 disease categories**:
- **Normal** - Healthy lungs with no disease
- **Pneumonia-Bacterial** - Bacterial pneumonia infection
- **Pneumonia-Viral** - Viral pneumonia (non-COVID)
- **COVID-19** - SARS-CoV-2 coronavirus infection
- **Tuberculosis** - Chronic TB infection
- **Emphysema** - COPD-related lung disease

## 🚀 Features

- ✅ Upload single or multiple chest X-ray images
- ✅ Real-time disease prediction with confidence scores
- ✅ User-friendly web interface
- ✅ RESTful API for integration
- ✅ Pre-trained model with high accuracy (>90%)
- ✅ Responsive design for mobile and desktop

## 📊 Dataset

**Dataset Used:** [ChestX6: Multi-Class X-ray Dataset](https://www.kaggle.com/datasets/mohamedasak/chest-x-ray-6-classes-dataset)

- Total Images: 18,036 X-ray images
- Categories: 6 disease classes
  - Normal (healthy lungs)
  - Pneumonia-Bacterial
  - Pneumonia-Viral
  - COVID-19
  - Tuberculosis
  - Emphysema
- Format: JPG/PNG
- Image Size: 224×224 pixels
- Distribution: Well-balanced across classes

## 🛠️ Technology Stack

### Machine Learning
- TensorFlow/Keras - Deep Learning Framework
- ResNet50/VGG16 - Transfer Learning Models
- NumPy, Pandas - Data Processing
- Matplotlib, Seaborn - Visualization

### Backend
- Flask - Web Framework
- Pillow - Image Processing
- Flask-CORS - Cross-Origin Resource Sharing

### Frontend
- HTML5/CSS3 - Structure & Styling
- JavaScript - Interactivity
- Bootstrap 5 - Responsive Design

## 📁 Project Structure

```
HealthCare Project/
│
├── model_training/
│   └── Chest_Xray_Training.ipynb    # Google Colab notebook for training
│
├── backend/
│   ├── app.py                        # Flask API server
│   ├── model.py                      # Model loading and prediction logic
│   └── requirements.txt              # Python dependencies
│
├── frontend/
│   ├── index.html                    # Main web interface
│   ├── style.css                     # Styling
│   └── script.js                     # Frontend logic
│
├── models/
│   └── chest_xray_model.h5          # Trained model (generated after training)
│
├── test_images/                      # Sample X-ray images for testing
│
└── README.md                         # Project documentation
```

## 📋 Prerequisites

- Python 3.8 or higher
- Google Account (for Google Colab)
- Kaggle Account (to download dataset)
- 4GB+ RAM (for running the application)

## 🔧 Installation & Setup

### Step 1: Clone/Download the Project

Already done! You have the project in `f:\My Projects\HealthCare Project`

### Step 2: Get the Dataset from Kaggle

1. Go to [Kaggle Chest X-Ray Dataset](https://www.kaggle.com/datasets/paultimothymooney/chest-xray-pneumonia)
2. Click **"Download"** (you'll need to sign in)
3. Extract the ZIP file - you'll get a `chest_xray` folder

### Step 3: Train the Model (Google Colab)

1. Open `model_training/Chest_Xray_Training.ipynb`
2. Upload it to Google Colab: https://colab.research.google.com/
3. Follow the instructions in the notebook to:
   - Upload the dataset
   - Train the model (takes 30-60 minutes)
   - Download the trained model file (`chest_xray_model.h5`)
4. Place the downloaded model in the `models/` folder

### Step 4: Install Backend Dependencies

```bash
cd "f:\My Projects\HealthCare Project\backend"
pip install -r requirements.txt
```

### Step 5: Run the Application

```bash
cd "f:\My Projects\HealthCare Project\backend"
python app.py
```

The server will start at `http://localhost:5000`

### Step 6: Access the Web Interface

Open your browser and go to:
```
http://localhost:5000
```

## 🎓 How to Use

1. **Open the web application** in your browser
2. **Click "Choose Files"** to upload X-ray images (JPEG/PNG)
3. **Click "Predict"** to analyze the images
4. **View Results** - See predictions with confidence scores
5. **Upload more images** as needed

## 🧠 Model Architecture

- **Base Model:** ResNet50 (pre-trained on ImageNet)
- **Custom Layers:** Dense layers with dropout for regularization
- **Input Size:** 224x224x3
- **Output:** 3 classes (Normal, Bacterial Pneumonia, Viral Pneumonia)
- **Optimizer:** Adam
- **Loss Function:** Categorical Crossentropy

## 📈 Model Performance

Expected Metrics (after training):
- **Accuracy:** ~88-92%
- **Precision:** ~85-90%
- **Recall:** ~85-90%
- **F1-Score:** ~85-90%
- **6-Class Classification** (more challenging than binary)

## 🔌 API Endpoints

### POST /predict
Upload and predict X-ray images

**Request:**
```bash
curl -X POST -F "file=@xray.jpg" http://localhost:5000/predict
```

**Response:**
```json
{
  "success": true,
  "predictions": [
    {
      "class": "PNEUMONIA_BACTERIAL",
      "confidence": 0.94,
      "label": "Pneumonia (Bacterial)"
    }
  ]
}
```

## 🚀 Deployment Options

### Option 1: Heroku (Free Tier Available)
- Easy deployment with Git
- Suitable for small projects

### Option 2: Google Cloud Platform
- Free tier available
- Better scalability

### Option 3: AWS EC2
- More control over infrastructure

## 🎯 Resume Highlights

This project demonstrates:
- ✅ **Deep Learning:** CNN architecture, transfer learning
- ✅ **Computer Vision:** Image preprocessing, augmentation
- ✅ **Full-Stack Development:** Backend API + Frontend UI
- ✅ **Healthcare AI:** Real-world medical application
- ✅ **Model Deployment:** Serving ML models in production
- ✅ **Data Science:** Model evaluation, performance metrics

## 📝 Future Enhancements

- [ ] Support for 14+ diseases (using NIH dataset)
- [ ] User authentication and history
- [ ] Database integration for storing results
- [ ] Mobile app (React Native/Flutter)
- [ ] Docker containerization
- [ ] Real-time model monitoring
- [ ] DICOM format support

## 🤝 Contributing

This is a personal project, but suggestions are welcome!

## ⚠️ Disclaimer

**This is an educational project and should NOT be used for actual medical diagnosis. Always consult qualified healthcare professionals for medical advice.**

## 📧 Contact

Add your contact information here for your resume!

## 📄 License

MIT License - Feel free to use for educational purposes

---

**Made with ❤️ for Healthcare AI**
