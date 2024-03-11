from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, Dropout, MaxPooling2D, Conv2D, Flatten

def create_model():
    model = Sequential([
        Conv2D(16, 3, padding='same', activation='relu', input_shape=(160, 120, 1)),
        MaxPooling2D(),
        Conv2D(32, 3, padding='same', activation='relu'),
        MaxPooling2D(),
        Conv2D(64, 3, padding='same', activation='relu'),
        MaxPooling2D(),
        Conv2D(64, 3, padding='same', activation='relu'),
        MaxPooling2D(),
        Conv2D(64, 3, padding='same', activation='relu'),
        MaxPooling2D(),

        Flatten(),
        Dense(764, activation='relu'),
        Dropout(0.1),
        Dense(100, activation='relu'),
        Dropout(0.1),
        Dense(50, activation='relu'),
        Dropout(0.1),
        Dense(1, activation='sigmoid')
    ])
    return model
