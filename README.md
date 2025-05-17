# Handwritten Digit Recognition

A web application that recognizes handwritten digits (0-9) drawn by the user on a canvas. The project uses a Deep Neural Network (DNN) trained on the MNIST dataset and provides a modern, interactive frontend.

---

## Features

- **Draw** digits on a canvas using your mouse.
- **Adjust brush size** for comfortable drawing.
- **Recognize** the digit with a single click.
- **Prediction history** is displayed in a neat table with timestamps.
- **Dynamic UI** with animated backgrounds and interactive effects.
- **Trail effect** follows your cursor for a fun experience.

---

## Project Structure

├── app.py # Flask backend for prediction 
├── new_model.py # Model training and saving script 
├── handwritten_digits.h5 # Saved trained model (generated after training) 
├── web.html # Main frontend HTML file ├── styles.css # CSS for dynamic and modern UI ├── script.js # JavaScript for drawing, prediction, and UI logic 
└── uploads/ # Temporary folder for uploaded images

## How It Works

1. **Frontend**  
   - User draws a digit on the canvas.
   - Clicks "Recognize" to send the drawing to the backend.
   - The predicted digit is displayed and added to the history table.

2. **Backend**  
   - Receives the image, preprocesses it (centers, resizes, normalizes).
   - Loads the trained DNN model and predicts the digit.
   - Returns the prediction as a JSON response.

3. **Model**  
   - A Deep Neural Network (DNN) with three hidden layers (512, 256, 128 neurons) and dropout for regularization.
   - Trained on the MNIST dataset for 50 epochs.

---
## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/handwritten-digit-recognition.git
cd handwritten-digit-recognition
