# 📡 API Documentation

Complete API reference for the Chest X-Ray Prediction System.

---

## Base URL

```
http://localhost:5000/api
```

---

## Authentication

Currently, the API does not require authentication. For production deployment, consider implementing:
- API Keys
- OAuth 2.0
- JWT Tokens

---

## Endpoints

### 1. Health Check

Check if the API server and model are running.

**Endpoint:** `GET /api/health`

**Response:**
```json
{
  "status": "healthy",
  "service": "Chest X-Ray Prediction API",
  "model_loaded": true,
  "version": "1.0.0"
}
```

**Example:**
```bash
curl http://localhost:5000/api/health
```

---

### 2. Model Information

Get detailed information about the loaded model.

**Endpoint:** `GET /api/model-info`

**Response:**
```json
{
  "loaded": true,
  "model_path": "../models/chest_xray_model.h5",
  "input_shape": [null, 224, 224, 3],
  "output_shape": [null, 2],
  "total_parameters": 24589314,
  "classes": {
    "0": "NORMAL",
    "1": "PNEUMONIA"
  }
}
```

**Example:**
```bash
curl http://localhost:5000/api/model-info
```

---

### 3. Predict Single/Multiple Images

Upload and predict chest X-ray images.

**Endpoint:** `POST /api/predict`

**Request:**
- Method: `POST`
- Content-Type: `multipart/form-data`
- Body: Image file(s) with key `file`

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| file | File | Yes | X-ray image (JPG, JPEG, PNG) |

**Constraints:**
- Maximum file size: 16MB per image
- Supported formats: JPG, JPEG, PNG
- Can upload multiple files at once

**Single Image Response:**
```json
{
  "success": true,
  "predicted_class": "PNEUMONIA",
  "confidence": 0.9456,
  "confidence_percentage": "94.56%",
  "all_probabilities": {
    "NORMAL": 0.0544,
    "PNEUMONIA": 0.9456
  },
  "interpretation": "High confidence - Signs of pneumonia detected. Recommend consultation with a physician.",
  "filename": "xray_image.jpg"
}
```

**Multiple Images Response:**
```json
{
  "success": true,
  "count": 2,
  "predictions": [
    {
      "success": true,
      "predicted_class": "NORMAL",
      "confidence": 0.9234,
      "confidence_percentage": "92.34%",
      "all_probabilities": {
        "NORMAL": 0.9234,
        "PNEUMONIA": 0.0766
      },
      "interpretation": "High confidence - Lungs appear normal. No signs of pneumonia detected.",
      "filename": "normal_xray.jpg"
    },
    {
      "success": true,
      "predicted_class": "PNEUMONIA",
      "confidence": 0.8891,
      "confidence_percentage": "88.91%",
      "all_probabilities": {
        "NORMAL": 0.1109,
        "PNEUMONIA": 0.8891
      },
      "interpretation": "High confidence - Signs of pneumonia detected. Recommend consultation with a physician.",
      "filename": "pneumonia_xray.jpg"
    }
  ]
}
```

**Error Response:**
```json
{
  "success": false,
  "error": "Model not loaded. Please train the model first."
}
```

**Example (cURL):**

Single image:
```bash
curl -X POST \
  -F "file=@/path/to/xray.jpg" \
  http://localhost:5000/api/predict
```

Multiple images:
```bash
curl -X POST \
  -F "file=@/path/to/xray1.jpg" \
  -F "file=@/path/to/xray2.jpg" \
  http://localhost:5000/api/predict
```

**Example (Python):**
```python
import requests

url = "http://localhost:5000/api/predict"
files = {"file": open("xray.jpg", "rb")}
response = requests.post(url, files=files)
print(response.json())
```

**Example (JavaScript):**
```javascript
const formData = new FormData();
formData.append('file', fileInput.files[0]);

fetch('http://localhost:5000/api/predict', {
  method: 'POST',
  body: formData
})
.then(response => response.json())
.then(data => console.log(data))
.catch(error => console.error('Error:', error));
```

---

## Response Codes

| Code | Description |
|------|-------------|
| 200 | Success |
| 400 | Bad Request (invalid file type, no file uploaded) |
| 413 | Payload Too Large (file > 16MB) |
| 500 | Internal Server Error |
| 503 | Service Unavailable (model not loaded) |

---

## Error Handling

All error responses follow this format:

```json
{
  "success": false,
  "error": "Error description here"
}
```

**Common Errors:**

1. **No file uploaded:**
```json
{
  "success": false,
  "error": "No file uploaded"
}
```

2. **Invalid file type:**
```json
{
  "success": false,
  "error": "Invalid file type. Only PNG, JPG, and JPEG are allowed."
}
```

3. **File too large:**
```json
{
  "success": false,
  "error": "File too large. Maximum size is 16MB."
}
```

4. **Model not loaded:**
```json
{
  "success": false,
  "error": "Model not loaded. Please train the model first.",
  "instructions": "Upload chest_xray_model.h5 to the models/ folder"
}
```

---

## Prediction Interpretation

The `interpretation` field provides human-readable analysis:

### Confidence Levels

- **High Confidence (>80%):** Strong prediction, reliable result
- **Moderate Confidence (60-80%):** Reasonable prediction, some uncertainty
- **Low Confidence (<60%):** Weak prediction, high uncertainty

### Example Interpretations

**Normal (High Confidence):**
```
"High confidence - Lungs appear normal. No signs of pneumonia detected."
```

**Pneumonia (Moderate Confidence):**
```
"Moderate confidence - Signs of pneumonia detected. Recommend consultation with a physician."
```

**Pneumonia (Low Confidence):**
```
"Low confidence - Signs of pneumonia detected. Recommend consultation with a physician."
```

---

## Rate Limiting

Currently, there are no rate limits on the API.

**For production, consider implementing:**
- Maximum requests per minute
- Maximum concurrent predictions
- Request queuing

---

## Best Practices

### 1. Image Quality
- Use high-resolution X-ray images
- Ensure proper contrast and brightness
- Avoid heavily compressed images

### 2. File Size
- Optimize images before upload
- Recommended size: 1-5MB
- Maximum allowed: 16MB

### 3. Batch Processing
- Upload multiple images in one request for efficiency
- Recommended batch size: 5-10 images
- Maximum: Limited by total payload size (16MB)

### 4. Error Handling
```python
import requests

def predict_xray(image_path):
    try:
        url = "http://localhost:5000/api/predict"
        files = {"file": open(image_path, "rb")}
        response = requests.post(url, files=files, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                return data
            else:
                print(f"Prediction failed: {data.get('error')}")
                return None
        else:
            print(f"HTTP Error: {response.status_code}")
            return None
            
    except requests.exceptions.Timeout:
        print("Request timed out")
        return None
    except Exception as e:
        print(f"Error: {str(e)}")
        return None
```

---

## Integration Examples

### Web Application (JavaScript/React)

```javascript
async function predictXray(file) {
  const formData = new FormData();
  formData.append('file', file);

  try {
    const response = await fetch('http://localhost:5000/api/predict', {
      method: 'POST',
      body: formData
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    
    if (data.success) {
      console.log('Prediction:', data.predicted_class);
      console.log('Confidence:', data.confidence_percentage);
      return data;
    } else {
      console.error('Prediction failed:', data.error);
      return null;
    }
  } catch (error) {
    console.error('Error:', error);
    return null;
  }
}
```

### Mobile App (Flutter/Dart)

```dart
import 'package:http/http.dart' as http;
import 'dart:convert';

Future<Map<String, dynamic>?> predictXray(File imageFile) async {
  var uri = Uri.parse('http://localhost:5000/api/predict');
  var request = http.MultipartRequest('POST', uri);
  
  request.files.add(
    await http.MultipartFile.fromPath('file', imageFile.path)
  );

  try {
    var streamedResponse = await request.send();
    var response = await http.Response.fromStream(streamedResponse);

    if (response.statusCode == 200) {
      var data = json.decode(response.body);
      if (data['success']) {
        return data;
      }
    }
    return null;
  } catch (e) {
    print('Error: $e');
    return null;
  }
}
```

### CLI Tool (Python)

```python
import requests
import sys
from pathlib import Path

def main():
    if len(sys.argv) < 2:
        print("Usage: python predict.py <image_path>")
        return

    image_path = Path(sys.argv[1])
    
    if not image_path.exists():
        print(f"Error: File not found: {image_path}")
        return

    url = "http://localhost:5000/api/predict"
    files = {"file": open(image_path, "rb")}
    
    print(f"Analyzing {image_path.name}...")
    response = requests.post(url, files=files)
    
    if response.status_code == 200:
        data = response.json()
        if data.get("success"):
            print(f"\n✅ Prediction: {data['predicted_class']}")
            print(f"📊 Confidence: {data['confidence_percentage']}")
            print(f"📋 {data['interpretation']}")
        else:
            print(f"\n❌ Error: {data.get('error')}")
    else:
        print(f"\n❌ HTTP Error: {response.status_code}")

if __name__ == "__main__":
    main()
```

---

## CORS Configuration

The API has CORS enabled for all origins.

**Production Configuration:**
```python
# In app.py
from flask_cors import CORS

# Allow specific origins only
CORS(app, origins=[
    "https://yourdomain.com",
    "https://app.yourdomain.com"
])
```

---

## Security Considerations

### For Production Deployment:

1. **Authentication:** Add API key or token-based auth
2. **HTTPS:** Use SSL/TLS encryption
3. **Input Validation:** Sanitize file uploads
4. **Rate Limiting:** Prevent abuse
5. **File Scanning:** Check for malicious files
6. **CORS:** Restrict allowed origins
7. **Logging:** Monitor API usage
8. **Error Messages:** Don't expose sensitive info

---

## Deployment

### Environment Variables

Create a `.env` file:
```
FLASK_ENV=production
MODEL_PATH=./models/chest_xray_model.h5
MAX_FILE_SIZE=16777216
ALLOWED_ORIGINS=https://yourdomain.com
```

### Production Server (Gunicorn)

```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

---

## Testing

### Test Health Endpoint
```bash
curl http://localhost:5000/api/health
```

### Test Prediction
```bash
curl -X POST \
  -F "file=@test_image.jpg" \
  http://localhost:5000/api/predict
```

---

## Support

For issues or questions:
- Check the error message in the response
- Review server logs
- Ensure model is properly loaded
- Verify file format and size

---

**API Version:** 1.0.0  
**Last Updated:** January 2026
