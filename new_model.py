import os
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
from scipy.ndimage import center_of_mass, shift

# Decide if to load an existing model or to train a new one
train_new_model = True
model_file = 'handwritten_digits.h5'  # Model file name
epochs = 50  # Number of epochs for training

if train_new_model:
    # Load the MNIST dataset
    mnist = tf.keras.datasets.mnist
    (X_train, y_train), (X_test, y_test) = mnist.load_data()

    # Normalize the data (scale pixel values to [0, 1])
    X_train = tf.keras.utils.normalize(X_train, axis=1)
    X_test = tf.keras.utils.normalize(X_test, axis=1)

    # Reshape the data to include the channel dimension
    X_train = X_train.reshape(X_train.shape[0], 28, 28, 1)  # Add channel dimension
    X_test = X_test.reshape(X_test.shape[0], 28, 28, 1)  # Add channel dimension

    # Create the neural network model
    model = tf.keras.models.Sequential([
    tf.keras.layers.Flatten(input_shape=(28, 28)),
    tf.keras.layers.Dense(units=512, activation='relu'),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(units=256, activation='relu'),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(units=128, activation='relu'),
    tf.keras.layers.Dense(units=10, activation='softmax')
])

    # Compile the model
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

    # Train the model
    history = model.fit(X_train, y_train, epochs=epochs, validation_data=(X_test, y_test))

    # Evaluate the model
    val_loss, val_acc = model.evaluate(X_test, y_test)
    print(f"Validation Loss: {val_loss}")
    print(f"Validation Accuracy: {val_acc}")

    # Save the model
    model.save(model_file)
    print(f"Model saved as {model_file}")

    # Plot training history
    plt.plot(history.history['accuracy'], label='Accuracy')
    plt.plot(history.history['loss'], label='Loss')
    plt.title('Training History')
    plt.xlabel('Epochs')
    plt.ylabel('Value')
    plt.legend()
    plt.show()

else:
    # Load the existing model
    if os.path.exists(model_file):
        model = tf.keras.models.load_model(model_file)
        print(f"Model loaded from {model_file}")
    else:
        print(f"Error: Model file {model_file} not found!")