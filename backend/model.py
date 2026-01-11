"""
Model Loading and Prediction Module
Handles loading the trained model and making predictions on X-ray images
"""

import numpy as np
from PIL import Image
import tensorflow as tf
from tensorflow.keras.models import load_model
import os
import json


class ChestXrayPredictor:
    """
    Class to handle chest X-ray image predictions
    """
    
    def __init__(self, model_path='../models/chest_xray_model.h5'):
        """
        Initialize the predictor with a trained model
        
        Args:
            model_path (str): Path to the trained model file
        """
        self.model_path = model_path
        self.model = None
        self.img_size = 224  # Must match training size
        # CRITICAL: Class order must match train_generator.class_indices from training
        # Based on ChestX6 dataset alphabetical folder sorting:
        self.class_labels = {
            0: 'Covid-19',
            1: 'Emphysema',
            2: 'Normal',
            3: 'Pneumonia-Bacterial',
            4: 'Pneumonia-Viral',
            5: 'Tuberculosis'
        }
        
        # Try to load the model
        self.load_model()
    
    def load_model(self):
        """
        Load the trained model from disk
        """
        try:
            if not os.path.exists(self.model_path):
                print(f"⚠️  Warning: Model file not found at {self.model_path}")
                print("Please train the model first using the Colab notebook.")
                return False
            
            print(f"📦 Loading model from {self.model_path}...")
            self.model = load_model(self.model_path)
            print("✅ Model loaded successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Error loading model: {str(e)}")
            return False
    
    def preprocess_image(self, image_file):
        """
        Preprocess image for prediction with universal normalization
        
        Args:
            image_file: File object or file path
            
        Returns:
            numpy array: Preprocessed image ready for prediction
        """
        try:
            # Open image
            if isinstance(image_file, str):
                img = Image.open(image_file)
            else:
                img = Image.open(image_file.stream)
            
            # Convert to RGB (in case image is grayscale)
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Convert to array for preprocessing
            img_array = np.array(img)
            
            # Apply CLAHE (Contrast Limited Adaptive Histogram Equalization)
            # This normalizes contrast across different X-ray sources for better generalization
            try:
                import cv2
                
                # Convert to LAB color space for better contrast enhancement
                lab = cv2.cvtColor(img_array, cv2.COLOR_RGB2LAB)
                l, a, b = cv2.split(lab)
                
                # Apply CLAHE to L channel (lightness)
                clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
                l = clahe.apply(l)
                
                # Merge back
                lab = cv2.merge([l, a, b])
                img_array = cv2.cvtColor(lab, cv2.COLOR_LAB2RGB)
                
                print("✓ CLAHE preprocessing applied")
            except ImportError:
                # Fallback: Simple histogram equalization using numpy
                print("⚠️ OpenCV not available, using basic normalization")
                # Normalize to 0-1 range per channel
                for i in range(3):
                    channel = img_array[:, :, i].astype(np.float32)
                    min_val, max_val = channel.min(), channel.max()
                    if max_val > min_val:
                        img_array[:, :, i] = ((channel - min_val) / (max_val - min_val) * 255).astype(np.uint8)
            
            # Convert back to PIL Image for resizing
            img = Image.fromarray(img_array.astype(np.uint8))
            
            # Resize to model input size
            img = img.resize((self.img_size, self.img_size))
            
            # Convert to array
            img_array = np.array(img)
            
            # Normalize pixel values to [0, 1]
            img_array = img_array.astype('float32') / 255.0
            
            # Add batch dimension
            img_array = np.expand_dims(img_array, axis=0)
            
            return img_array
            
        except Exception as e:
            print(f"❌ Error preprocessing image: {str(e)}")
            return None
    
    def predict(self, image_file):
        """
        Make prediction on a single image
        
        Args:
            image_file: File object or file path
            
        Returns:
            dict: Prediction results with class and confidence
        """
        if self.model is None:
            return {
                'success': False,
                'error': 'Model not loaded. Please train the model first.'
            }
        
        try:
            # Preprocess image
            img_array = self.preprocess_image(image_file)
            
            if img_array is None:
                return {
                    'success': False,
                    'error': 'Failed to preprocess image'
                }
            
            # Make prediction
            predictions = self.model.predict(img_array, verbose=0)
            
            # Get predicted class and confidence
            predicted_class = int(np.argmax(predictions[0]))
            confidence = float(predictions[0][predicted_class])
            
            # Get class label
            class_label = self.class_labels.get(predicted_class, 'UNKNOWN')
            
            # Get all class probabilities
            all_probabilities = {
                self.class_labels[i]: float(predictions[0][i])
                for i in range(len(predictions[0]))
            }
            
            return {
                'success': True,
                'predicted_class': class_label,
                'confidence': confidence,
                'confidence_percentage': f"{confidence * 100:.2f}%",
                'all_probabilities': all_probabilities,
                'interpretation': self._interpret_result(class_label, confidence)
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Prediction failed: {str(e)}'
            }
    
    def predict_batch(self, image_files):
        """
        Make predictions on multiple images
        
        Args:
            image_files: List of file objects or file paths
            
        Returns:
            list: List of prediction results
        """
        results = []
        
        for img_file in image_files:
            result = self.predict(img_file)
            results.append(result)
        
        return results
    
    def _interpret_result(self, class_label, confidence):
        """
        Provide interpretation of the prediction
        
        Args:
            class_label (str): Predicted class
            confidence (float): Prediction confidence
            
        Returns:
            str: Human-readable interpretation
        """
        if confidence < 0.6:
            certainty = "Low confidence"
        elif confidence < 0.8:
            certainty = "Moderate confidence"
        else:
            certainty = "High confidence"
        
        interpretations = {
            'Normal': f"{certainty} - Lungs appear healthy. No signs of disease detected.",
            'Pneumonia-Bacterial': f"{certainty} - Bacterial pneumonia detected. Shows dense consolidations. Urgent medical consultation recommended.",
            'Pneumonia-Viral': f"{certainty} - Viral pneumonia detected. Shows diffuse infiltrates. Medical consultation recommended.",
            'Covid-19': f"{certainty} - COVID-19 detected. Shows bilateral ground-glass opacities. Immediate isolation and medical care required.",
            'COVID-19': f"{certainty} - COVID-19 detected. Shows bilateral ground-glass opacities. Immediate isolation and medical care required.",
            'Tuberculosis': f"{certainty} - Tuberculosis detected. Shows characteristic TB patterns. Immediate medical evaluation and treatment needed.",
            'Emphysema': f"{certainty} - Emphysema detected. Shows hyperinflation and COPD patterns. Pulmonologist consultation recommended."
        }
        
        return interpretations.get(class_label, "Unable to classify image.")
    
    def get_model_info(self):
        """
        Get information about the loaded model
        
        Returns:
            dict: Model information
        """
        if self.model is None:
            return {
                'loaded': False,
                'message': 'Model not loaded'
            }
        
        return {
            'loaded': True,
            'model_path': self.model_path,
            'input_shape': self.model.input_shape,
            'output_shape': self.model.output_shape,
            'total_parameters': self.model.count_params(),
            'classes': self.class_labels
        }


# Create a global instance
predictor = ChestXrayPredictor()


if __name__ == '__main__':
    # Test the predictor
    info = predictor.get_model_info()
    print("\n📊 Model Information:")
    print(json.dumps(info, indent=2))
    
    # Test with a sample image (if available)
    test_image_path = '../test_images/sample_xray.jpg'
    if os.path.exists(test_image_path):
        print(f"\n🔍 Testing prediction on {test_image_path}...")
        result = predictor.predict(test_image_path)
        print(json.dumps(result, indent=2))
    else:
        print(f"\n⚠️  No test image found at {test_image_path}")
