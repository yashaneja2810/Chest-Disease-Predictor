// Global variables
let selectedFiles = [];
const API_BASE_URL = 'http://localhost:5000/api';

// DOM Elements
const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('fileInput');
const browseBtn = document.getElementById('browseBtn');
const previewSection = document.getElementById('previewSection');
const previewGrid = document.getElementById('previewGrid');
const imageCount = document.getElementById('imageCount');
const clearBtn = document.getElementById('clearBtn');
const predictBtn = document.getElementById('predictBtn');
const predictBtnText = document.getElementById('predictBtnText');
const spinner = document.getElementById('spinner');
const resultsSection = document.getElementById('resultsSection');
const resultsGrid = document.getElementById('resultsGrid');
const modelStatus = document.getElementById('modelStatus');
const detailModal = document.getElementById('detailModal');
const modalClose = document.getElementById('modalClose');

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    initializeEventListeners();
    checkModelStatus();
});

// Event Listeners
function initializeEventListeners() {
    // Browse button click
    browseBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        fileInput.click();
    });

    // Upload area click
    uploadArea.addEventListener('click', () => {
        fileInput.click();
    });

    // File input change
    fileInput.addEventListener('change', handleFileSelect);

    // Drag and drop
    uploadArea.addEventListener('dragover', handleDragOver);
    uploadArea.addEventListener('dragleave', handleDragLeave);
    uploadArea.addEventListener('drop', handleDrop);

    // Clear button
    clearBtn.addEventListener('click', clearSelection);

    // Predict button
    predictBtn.addEventListener('click', handlePredict);

    // Modal close
    modalClose.addEventListener('click', () => {
        detailModal.classList.remove('active');
    });

    // Click outside modal to close
    detailModal.addEventListener('click', (e) => {
        if (e.target === detailModal) {
            detailModal.classList.remove('active');
        }
    });
}

// Check model status
async function checkModelStatus() {
    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        const data = await response.json();

        const statusElement = modelStatus.querySelector('.status-text');
        
        if (data.model_loaded) {
            modelStatus.classList.add('active');
            modelStatus.classList.remove('error');
            statusElement.textContent = 'Model Ready';
        } else {
            modelStatus.classList.add('error');
            modelStatus.classList.remove('active');
            statusElement.textContent = 'Model Not Loaded';
        }
    } catch (error) {
        modelStatus.classList.add('error');
        modelStatus.classList.remove('active');
        modelStatus.querySelector('.status-text').textContent = 'Server Offline';
    }
}

// Handle file selection
function handleFileSelect(e) {
    const files = Array.from(e.target.files);
    addFiles(files);
}

// Handle drag over
function handleDragOver(e) {
    e.preventDefault();
    uploadArea.classList.add('drag-over');
}

// Handle drag leave
function handleDragLeave(e) {
    e.preventDefault();
    uploadArea.classList.remove('drag-over');
}

// Handle drop
function handleDrop(e) {
    e.preventDefault();
    uploadArea.classList.remove('drag-over');
    
    const files = Array.from(e.dataTransfer.files);
    addFiles(files);
}

// Add files to selection
function addFiles(files) {
    // Filter valid image files
    const validFiles = files.filter(file => {
        const validTypes = ['image/jpeg', 'image/jpg', 'image/png'];
        const maxSize = 16 * 1024 * 1024; // 16MB
        
        if (!validTypes.includes(file.type)) {
            showNotification('Invalid file type. Only JPG, JPEG, and PNG are allowed.', 'error');
            return false;
        }
        
        if (file.size > maxSize) {
            showNotification(`File ${file.name} is too large. Max size is 16MB.`, 'error');
            return false;
        }
        
        return true;
    });

    if (validFiles.length === 0) return;

    // Add to selected files
    selectedFiles = [...selectedFiles, ...validFiles];
    updatePreview();
}

// Update preview
function updatePreview() {
    if (selectedFiles.length === 0) {
        previewSection.style.display = 'none';
        return;
    }

    previewSection.style.display = 'block';
    imageCount.textContent = selectedFiles.length;
    previewGrid.innerHTML = '';

    selectedFiles.forEach((file, index) => {
        const reader = new FileReader();
        
        reader.onload = (e) => {
            const previewItem = document.createElement('div');
            previewItem.className = 'preview-item';
            previewItem.innerHTML = `
                <img src="${e.target.result}" alt="${file.name}">
                <button class="preview-item-remove" data-index="${index}">×</button>
            `;
            
            // Add remove listener
            const removeBtn = previewItem.querySelector('.preview-item-remove');
            removeBtn.addEventListener('click', () => removeFile(index));
            
            previewGrid.appendChild(previewItem);
        };
        
        reader.readAsDataURL(file);
    });
}

// Remove file
function removeFile(index) {
    selectedFiles.splice(index, 1);
    updatePreview();
}

// Clear selection
function clearSelection() {
    selectedFiles = [];
    fileInput.value = '';
    updatePreview();
    resultsSection.style.display = 'none';
    resultsGrid.innerHTML = '';
}

// Handle prediction
async function handlePredict() {
    if (selectedFiles.length === 0) {
        showNotification('Please select at least one image.', 'error');
        return;
    }

    // Disable button and show spinner
    predictBtn.disabled = true;
    predictBtnText.textContent = 'Analyzing...';
    spinner.style.display = 'inline-block';

    // Create form data
    const formData = new FormData();
    selectedFiles.forEach(file => {
        formData.append('file', file);
    });

    try {
        const response = await fetch(`${API_BASE_URL}/predict`, {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Prediction failed');
        }

        // Display results
        displayResults(data);
        showNotification('Prediction completed successfully!', 'success');

    } catch (error) {
        showNotification(error.message, 'error');
        console.error('Prediction error:', error);
    } finally {
        // Re-enable button
        predictBtn.disabled = false;
        predictBtnText.textContent = 'Predict';
        spinner.style.display = 'none';
    }
}

// Display results
function displayResults(data) {
    resultsSection.style.display = 'block';
    resultsGrid.innerHTML = '';

    // Handle both single and multiple results
    const predictions = data.predictions || [data];

    predictions.forEach((result, index) => {
        if (!result.success) {
            const errorCard = createErrorCard(result);
            resultsGrid.appendChild(errorCard);
            return;
        }

        const resultCard = createResultCard(result, index);
        resultsGrid.appendChild(resultCard);
    });

    // Scroll to results
    resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

// Create result card
function createResultCard(result, index) {
    const card = document.createElement('div');
    card.className = 'result-card';

    const isNormal = result.predicted_class === 'Normal';
    const confidence = result.confidence;
    
    let confidenceClass = 'high';
    if (confidence < 0.6) confidenceClass = 'low';
    else if (confidence < 0.8) confidenceClass = 'medium';

    // Get image preview
    const imageUrl = selectedFiles[index] ? URL.createObjectURL(selectedFiles[index]) : '';

    // Map disease names to display info
    const diseaseDisplay = {
        'Normal': { emoji: '✅', text: 'NORMAL', class: 'normal' },
        'Covid-19': { emoji: '🦠', text: 'COVID-19', class: 'covid' },
        'Emphysema': { emoji: '🫁', text: 'EMPHYSEMA', class: 'disease' },
        'Pneumonia-Bacterial': { emoji: '⚠️', text: 'PNEUMONIA (Bacterial)', class: 'pneumonia' },
        'Pneumonia-Viral': { emoji: '⚠️', text: 'PNEUMONIA (Viral)', class: 'pneumonia' },
        'Tuberculosis': { emoji: '🔴', text: 'TUBERCULOSIS', class: 'disease' }
    };

    const display = diseaseDisplay[result.predicted_class] || { emoji: '❓', text: result.predicted_class.toUpperCase(), class: 'disease' };

    card.innerHTML = `
        ${imageUrl ? `<img src="${imageUrl}" alt="X-Ray" class="result-image">` : ''}
        <div class="result-content">
            <div class="result-header">
                <div class="result-label ${display.class}">
                    ${display.emoji} ${display.text}
                </div>
                <div class="result-confidence ${confidenceClass}">
                    ${result.confidence_percentage}
                </div>
            </div>
            <div class="result-interpretation">
                ${result.interpretation}
            </div>
        </div>
    `;

    // Add click event for detailed view
    card.addEventListener('click', () => showDetailedResult(result, imageUrl));

    return card;
}

// Create error card
function createErrorCard(result) {
    const card = document.createElement('div');
    card.className = 'result-card';
    card.innerHTML = `
        <div class="result-content">
            <div class="error-message">
                <strong>Error:</strong> ${result.error}
            </div>
        </div>
    `;
    return card;
}

// Show detailed result in modal
function showDetailedResult(result, imageUrl) {
    const modalBody = document.getElementById('modalBody');
    
    const isNormal = result.predicted_class === 'Normal';
    
    modalBody.innerHTML = `
        ${imageUrl ? `<img src="${imageUrl}" alt="X-Ray" style="width: 100%; border-radius: 8px; margin-bottom: 24px;">` : ''}
        
        <h2 style="margin-bottom: 16px; color: ${isNormal ? 'var(--success-color)' : 'var(--danger-color)'};">
            ${isNormal ? '✅ Normal Chest X-Ray' : '⚠️ Pneumonia Detected'}
        </h2>
        
        <div style="background: var(--bg-secondary); padding: 16px; border-radius: 8px; margin-bottom: 16px;">
            <h3 style="margin-bottom: 12px; font-size: 16px;">Prediction Details</h3>
            <p style="margin-bottom: 8px;"><strong>Predicted Class:</strong> ${result.predicted_class}</p>
            <p style="margin-bottom: 8px;"><strong>Confidence:</strong> ${result.confidence_percentage}</p>
        </div>
        
        <div style="background: var(--bg-secondary); padding: 16px; border-radius: 8px; margin-bottom: 16px;">
            <h3 style="margin-bottom: 12px; font-size: 16px;">Class Probabilities</h3>
            ${Object.entries(result.all_probabilities).map(([label, prob]) => `
                <div style="margin-bottom: 8px;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
                        <span>${label}</span>
                        <span><strong>${(prob * 100).toFixed(2)}%</strong></span>
                    </div>
                    <div style="background: var(--border-color); height: 8px; border-radius: 4px; overflow: hidden;">
                        <div style="background: var(--primary-color); height: 100%; width: ${prob * 100}%; transition: width 0.3s ease;"></div>
                    </div>
                </div>
            `).join('')}
        </div>
        
        <div style="background: #FEF3C7; border: 2px solid #FCD34D; padding: 16px; border-radius: 8px;">
            <p style="color: #78350F; font-size: 14px; margin: 0;">
                <strong>⚠️ Important:</strong> ${result.interpretation} This is an AI-based analysis for educational purposes only. Always consult healthcare professionals for medical diagnosis.
            </p>
        </div>
    `;
    
    detailModal.classList.add('active');
}

// Show notification
function showNotification(message, type = 'info') {
    // Remove existing notifications
    const existingNotif = document.querySelector('.notification');
    if (existingNotif) {
        existingNotif.remove();
    }

    // Create notification
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.style.cssText = `
        position: fixed;
        top: 80px;
        right: 24px;
        background: ${type === 'error' ? '#FEE2E2' : type === 'success' ? '#DCFCE7' : '#EFF6FF'};
        border: 2px solid ${type === 'error' ? '#EF4444' : type === 'success' ? '#10B981' : '#3B82F6'};
        color: ${type === 'error' ? '#991B1B' : type === 'success' ? '#166534' : '#1E40AF'};
        padding: 16px 24px;
        border-radius: 8px;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        z-index: 3000;
        max-width: 400px;
        animation: slideIn 0.3s ease;
    `;
    
    notification.textContent = message;
    document.body.appendChild(notification);

    // Auto remove after 5 seconds
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    }, 5000);
}

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(400px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);
