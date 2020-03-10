import tensorflow as tf
import tensorflow.keras as keras

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense


model = Sequential()
model.add(Embedding(128, 128, input_length=40))
model.add(LSTM(128))
model.add(Dense(128, activation='softmax'))

model.compile(loss="categorical_crossentropy", optimizer='adam', metrics=['accuracy'])

print(model.summary())