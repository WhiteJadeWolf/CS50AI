import csv
import tensorflow as tf

from sklearn.model_selection import train_test_split

# Read data in from file
with open("banknotes.csv") as f:
    reader = csv.reader(f)
    next(reader)

    data = []
    for row in reader:
        data.append({
            "evidence": [float(cell) for cell in row[:4]],
            "label": 1 if row[4] == "0" else 0
        })

# Separate data into training and testing groups
evidence = [row["evidence"] for row in data]
labels = [row["label"] for row in data]
X_training, X_testing, y_training, y_testing = train_test_split(
    evidence, labels, test_size=0.4
)

# Create a neural network
model = tf.keras.models.Sequential()

""" keras is TensorFlow's high-level neural network API.
tf.keras = TensorFlow's built-in version of Keras.
It provides classes and functions for building deep learning models easily, such as:
Layers (Dense, Conv2D, LSTM…)
Optimizers
Loss functions
Model architectures (Sequential, Functional, Subclassing) 

Sequential is a model class that allows you to build a neural network layer by layer in a straight line.
Input → Layer1 → Layer2 → Layer3 → ... → Output    """

# Add a hidden layer with 8 units, with ReLU activation
model.add(tf.keras.layers.Dense(8, input_shape=(4,), activation="relu")) 

""" Dense is a fully connected neural network layer, meaning every input neuron connects to every output neuron.

    8 means the layer will have 8 neurons/units
    
    input_shape tells the model the shape of one input sample.
    input_shape=(4,) means:
        Each input has 4 features (4 numbers).
        Example input: [5.1, 3.5, 1.4, 0.2]
        You ONLY specify input_shape for the first layer.
        Future layers automatically infer the shape.
        
    activation func is ReLU i.e. relu(x)=max(0,x)  """

# Add output layer with 1 unit, with sigmoid activation
model.add(tf.keras.layers.Dense(1, activation="sigmoid"))

# Train neural network
model.compile(
    optimizer="adam",
    loss="binary_crossentropy",
    metrics=["accuracy"]
)

""" The optimizer adjusts the model's weights to reduce the loss.
    Adam = Adaptive Moment Estimation
    It automatically adjusts learning rate for each parameter
    default good choice for almost any model.
    
    The loss function measures how wrong the model is.
    binary crossentropy calculates loss as  loss = -[y*log(p) + (1-y)*log(1-p)]
    We use binary crossentropy when we have two classes (binary classification), output layer has 1 unit with sigmoid activation
    Our banknote authentication dataset is binary (real vs fake), so this is perfect.
    
    Metrics tell you how well your model is performing, but they do not affect learning.
    "accuracy" means during training and testing, TensorFlow will display accuracy.
    Useful for understanding performance, but not used for weight updates.  """
    
model.fit(X_training, y_training, epochs=20)

""" 1 epoch = the model sees the entire training dataset once
    If your training set has 1,000 samples:
        1 epoch → the model goes through all 1,000 samples once
        20 epochs → the model goes through all 1,000 samples 20 times
    Each time it sees the entire dataset, it updates its weights to reduce the loss. """

# Evaluate how well model performs
model.evaluate(X_testing, y_testing, verbose=2)

""" the parameter verbose controls how much output the function prints while running.

    verbose can take three values:

    VALUE	            MEANING	                                    WHAT'S SEEN ONSCREEN
    0	                Silent	                                    No output at all
    1	                Progress bar	                            A live progress bar (default)
    2	                One line per epoch / no progress bar	    Clean, short output   """
