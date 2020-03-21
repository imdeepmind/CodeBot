import tensorflow as tf
import tensorflow.keras as keras

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense

from generator import train_generator, validation_generator, test_generator

BATCH_SIZE = 32
TRAIN_SIZE = 33274973
VALIDATION_SIZE = 4150122
TEST_SIZE = 3870306


train_g = train_generator(BATCH_SIZE)
# validation_g = validation_generator(BATCH_SIZE)
# test_g = test_generator(BATCH_SIZE)

model = Sequential()
model.add(Embedding(128, 128, input_length=40))
model.add(LSTM(128))
model.add(Dense(128, activation='softmax'))

model.compile(loss="categorical_crossentropy", optimizer='adam', metrics=['accuracy'])

print(model.summary())


model.fit_generator(train_g, 
					steps_per_epoch=TRAIN_SIZE // BATCH_SIZE,
					verbose=1,
					epochs=5)