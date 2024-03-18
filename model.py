from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, Dropout, MaxPooling2D, Conv2D, Flatten, Rescaling

def create_model():
    model = Sequential([
        # Rescaling(1.0/255, input_shape=(60, 80, 1)),
        Conv2D(64, 3, padding='same', activation='relu', input_shape=(60, 80, 1)),
        MaxPooling2D(),

        Flatten(),
        Dense(240, activation='relu'),
        Dense(32, activation='relu'),
        Dense(1, activation='sigmoid')
    ])

    return model