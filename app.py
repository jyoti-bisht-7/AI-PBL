from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import tensorflow as tf
import numpy as np
import cv2
import os
import os
from scipy.ndimage import center_of_mass, shift

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Allow cross-origin requests

# Load the trained model
model = tf.keras.models.load_model('handwritten_digits.h5')

# Create uploads folder
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    # Serve the web.html file when accessing the root URL
    return send_from_directory('.', 'web.html')

def center_image(img):
    """
    Centers the digit in the image by shifting it based on its center of mass.
    """
    cy, cx = center_of_mass(img)  # Find the center of mass
    rows, cols = img.shape
    shift_x = cols // 2 - int(cx)
    shift_y = rows // 2 - int(cy)
    return shift(img, shift=(shift_y, shift_x), cval=0)

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)
    
    try:
        # Read and preprocess the image
        img = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
        img = np.invert(img) # Invert colors
        img = center_image(img) # Center the digit
        img = cv2.resize(img, (28, 28))  # Resize to 28x28
        img = img / 255.0  # Normalize pixel values
        img = img.reshape(1, 28, 28, 1)  # Add channel dimension

        # Make prediction
        prediction = model.predict(img)
        result = int(np.argmax(prediction))  # Get the predicted class
        
        return jsonify({'prediction': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal Server Error'}), 500


@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not Found'}), 404


# Run Flask app
if __name__ == '__main__':
    app.run(debug=True)