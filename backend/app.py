"""
Flask Backend API for Chest X-Ray Disease Prediction
Provides REST API endpoints for image upload and prediction
"""

from flask import Flask, request, jsonify, send_from_directory, render_template_string
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
from model import predictor
import json

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for frontend requests

# Configuration
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Create upload folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


def allowed_file(filename):
    """
    Check if file extension is allowed
    
    Args:
        filename (str): Name of the file
        
    Returns:
        bool: True if allowed, False otherwise
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    """
    Serve the main HTML page
    """
    # Serve index.html from frontend folder
    frontend_path = os.path.join(os.path.dirname(__file__), '..', 'frontend')
    return send_from_directory(frontend_path, 'index.html')


@app.route('/style.css')
def serve_css():
    """
    Serve CSS file
    """
    frontend_path = os.path.join(os.path.dirname(__file__), '..', 'frontend')
    return send_from_directory(frontend_path, 'style.css')


@app.route('/script.js')
def serve_js():
    """
    Serve JavaScript file
    """
    frontend_path = os.path.join(os.path.dirname(__file__), '..', 'frontend')
    return send_from_directory(frontend_path, 'script.js')


@app.route('/favicon.ico')
def favicon():
    """
    Return empty favicon to prevent 404 errors
    """
    return '', 204


@app.route('/api/debug', methods=['GET'])
def debug_info():
    """
    Debug endpoint to check model info
    """
    import numpy as np
    
    # Create test prediction with random data
    test_input = np.random.rand(1, 224, 224, 3).astype('float32')
    test_pred = predictor.model.predict(test_input, verbose=0)
    
    return jsonify({
        'model_loaded': predictor.model is not None,
        'class_labels': predictor.class_labels,
        'test_prediction_shape': test_pred.shape,
        'test_prediction_sum': float(np.sum(test_pred[0])),
        'test_max_index': int(np.argmax(test_pred[0])),
        'test_max_value': float(np.max(test_pred[0]))
    })


@app.route('/api/health', methods=['GET'])
def health_check():
    """
    Health check endpoint
    
    Returns:
        JSON: Server status and model information
    """
    model_info = predictor.get_model_info()
    
    return jsonify({
        'status': 'healthy',
        'service': 'Chest X-Ray Prediction API',
        'model_loaded': model_info['loaded'],
        'version': '1.0.0'
    })


@app.route('/api/model-info', methods=['GET'])
def model_info():
    """
    Get detailed model information
    
    Returns:
        JSON: Model details
    """
    info = predictor.get_model_info()
    return jsonify(info)


@app.route('/api/predict', methods=['POST'])
def predict():
    """
    Predict disease from uploaded X-ray image(s)
    
    Expects:
        file: Image file(s) in form data
        
    Returns:
        JSON: Prediction results
    """
    try:
        # Check if model is loaded
        if not predictor.model:
            return jsonify({
                'success': False,
                'error': 'Model not loaded. Please train the model first using the Colab notebook.',
                'instructions': 'Upload chest_xray_model.h5 to the models/ folder'
            }), 503
        
        # Check if files were uploaded
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No file uploaded'
            }), 400
        
        files = request.files.getlist('file')
        
        if len(files) == 0:
            return jsonify({
                'success': False,
                'error': 'No files selected'
            }), 400
        
        results = []
        
        for file in files:
            # Check if file is empty
            if file.filename == '':
                continue
            
            # Check if file type is allowed
            if not allowed_file(file.filename):
                results.append({
                    'filename': file.filename,
                    'success': False,
                    'error': 'Invalid file type. Only PNG, JPG, and JPEG are allowed.'
                })
                continue
            
            # Save file temporarily
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Make prediction
            prediction_result = predictor.predict(filepath)
            prediction_result['filename'] = filename
            
            results.append(prediction_result)
            
            # Clean up uploaded file
            try:
                os.remove(filepath)
            except:
                pass
        
        # Return results
        if len(results) == 1:
            return jsonify(results[0])
        else:
            return jsonify({
                'success': True,
                'count': len(results),
                'predictions': results
            })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        }), 500


@app.route('/api/batch-predict', methods=['POST'])
def batch_predict():
    """
    Predict diseases from multiple X-ray images
    
    Expects:
        files: Multiple image files in form data
        
    Returns:
        JSON: List of prediction results
    """
    try:
        # Check if model is loaded
        if not predictor.model:
            return jsonify({
                'success': False,
                'error': 'Model not loaded. Please train the model first.'
            }), 503
        
        # Get all uploaded files
        files = request.files.getlist('files')
        
        if len(files) == 0:
            return jsonify({
                'success': False,
                'error': 'No files uploaded'
            }), 400
        
        results = []
        
        for file in files:
            if file and allowed_file(file.filename):
                # Make prediction
                prediction = predictor.predict(file)
                prediction['filename'] = secure_filename(file.filename)
                results.append(prediction)
        
        return jsonify({
            'success': True,
            'count': len(results),
            'predictions': results
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.errorhandler(413)
def request_entity_too_large(error):
    """
    Handle file too large error
    """
    return jsonify({
        'success': False,
        'error': 'File too large. Maximum size is 16MB.'
    }), 413


@app.errorhandler(404)
def not_found(error):
    """
    Handle 404 errors
    """
    return jsonify({
        'success': False,
        'error': 'Endpoint not found'
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """
    Handle 500 errors
    """
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500


if __name__ == '__main__':
    print("\n" + "="*60)
    print("🏥 CHEST X-RAY DISEASE PREDICTION API")
    print("="*60)
    print("\n📊 Model Status:")
    
    model_info = predictor.get_model_info()
    if model_info['loaded']:
        print("  ✅ Model loaded successfully!")
        print(f"  📁 Model path: {model_info['model_path']}")
        print(f"  🧠 Total parameters: {model_info['total_parameters']:,}")
        print(f"  📋 Classes: {list(model_info['classes'].values())}")
    else:
        print("  ⚠️  Model not loaded!")
        print("  📝 Instructions:")
        print("     1. Open model_training/Chest_Xray_Training.ipynb in Google Colab")
        print("     2. Run all cells to train the model")
        print("     3. Download chest_xray_model.h5")
        print("     4. Place it in the models/ folder")
    
    print("\n🌐 Server Configuration:")
    print("  • Host: http://localhost:5000")
    print("  • Max file size: 16MB")
    print("  • Allowed formats: PNG, JPG, JPEG")
    
    print("\n📡 API Endpoints:")
    print("  • GET  /api/health       - Health check")
    print("  • GET  /api/model-info   - Model information")
    print("  • POST /api/predict      - Single/multiple image prediction")
    
    print("\n🚀 Starting server...")
    print("="*60 + "\n")
    
    # Run the Flask app
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
        use_reloader=False  # Prevent double initialization
    )
