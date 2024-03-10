from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, Dropout, MaxPooling2D, Conv2D, Flatten

def create_model():
    model = Sequential([
        Conv2D(16, 3, padding='same', activation='relu', input_shape=(160, 120, 1)),
        MaxPooling2D(),
        Conv2D(32, 3, padding='same', activation='relu'),
        MaxPooling2D(),

        Flatten(),
        Dense(784, activation='relu'),
        Dense(150, activation='relu'),
        Dense(64, activation='relu'),
        Dense(16, activation='relu'),
        Dense(2, activation='sigmoid')
    ])
    return model
