from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, Dropout, MaxPooling2D, Conv2D, Flatten, Rescaling

def create_model():
    model = Sequential([
        Rescaling(1.0/255, input_shape=(120, 160, 1)),
        Conv2D(16, 3, padding='same', activation='relu'),
        MaxPooling2D(),

        Flatten(),
        # before was 1164, 512, 240
        Dense(32, activation='relu'),
        Dense(16, activation='relu'),
        Dense(1, activation='sigmoid')
    ])
    return model