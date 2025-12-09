import sys
import tensorflow as tf

# Use MNIST handwriting dataset
mnist = tf.keras.datasets.mnist

# Prepare data for training
(x_train, y_train), (x_test, y_test) = mnist.load_data()
x_train, x_test = x_train / 255.0, x_test / 255.0
y_train = tf.keras.utils.to_categorical(y_train)
y_test = tf.keras.utils.to_categorical(y_test)
x_train = x_train.reshape(
    x_train.shape[0], x_train.shape[1], x_train.shape[2], 1
)
x_test = x_test.reshape(
    x_test.shape[0], x_test.shape[1], x_test.shape[2], 1
)

# Create a convolutional neural network
model = tf.keras.models.Sequential([  # another way to add layers in a sequential NN model in tf is to add the layers as a list as input to the model 

    # Convolutional layer. Learn 32 filters using a 3x3 kernel
    tf.keras.layers.Conv2D(
        32, (3, 3), activation="relu", input_shape=(28, 28, 1) #  32 different filters, each filter/kernel being a 3x3 kernel matrix. Input image is 28x28 px with 1 channel(color) value (black or white). For color image we have 3 channel values so in that case itd be (28,28,3)
    ),

    # Max-pooling layer, using 2x2 pool size
    tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),

    # Flatten units
    tf.keras.layers.Flatten(),

    # Add a hidden layer with dropout to avoid overfitting
    tf.keras.layers.Dense(128, activation="relu"),
    tf.keras.layers.Dropout(0.5),

    # Add an output layer with output units for all 10 digits (0-9)
    tf.keras.layers.Dense(10, activation="softmax")
    
    #  Softmax is an activation function commonly used in the output layer of multi-class classification neural networks. It converts raw scores (logits) into probabilities that sum to 1. 
    # Given a set of numbers (like outputs of a Dense layer), softmax:
    #     Exponentiates them (makes them positive and larger if they're bigger)
    #     Normalizes them (so the sum becomes 1)
    # This turns the outputs into a probability distribution.
])

# Train neural network
model.compile(
    optimizer="adam",
    loss="categorical_crossentropy",
    metrics=["accuracy"]
)
model.fit(x_train, y_train, epochs=10)

# Evaluate neural network performance
model.evaluate(x_test,  y_test, verbose=2)

# Save model to file for future use without training ts all over again
if len(sys.argv) == 2:
    filename = sys.argv[1]
    model.save(filename)
    print(f"Model saved to {filename}.")
