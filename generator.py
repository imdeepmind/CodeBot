import sqlite3
import numpy as np

train_couter = 0
validation_counter = 0
test_counter = 0

conn = sqlite3.connect('data/code.db')
c = conn.cursor()

def ont_hot(sequences, nexts, batch_size):
    x = np.zeros((batch_size, 40, 128), dtype=np.bool)
    y = np.zeros((batch_size, 128), dtype=np.bool)

    for i, sequence in enumerate(sequences):
    	if nexts[i] < 0 or nexts[i] > 128:
    		y[i, 97] = 1
    	else:
    		y[i, nexts[i]] = 1

    return np.array(sequences), y

def train_generator(batch_size):
	global train_couter

	while True:
		sql = f"SELECT sequence, next FROM code_sequences WHERE state = 'tr' LIMIT {batch_size} OFFSET {batch_size * train_couter}"

		train_couter += 1

		c.execute(sql)

		rows = c.fetchall()

		sequences = []
		nexts = []

		for sequence, next in rows:
			temp = []
			for char in sequence:
				temp.append(ord(char))

			sequences.append(temp)
			nexts.append(ord(next))

		x,y =  ont_hot(sequences, nexts, batch_size)

		assert x.shape == (batch_size, 40), "Invalid dimension for Input X"
		assert y.shape == (batch_size, 128), "Invalid dimension for Output Y"

		yield  x, y

def validation_generator(batch_size):
	global validation_counter

	while True:
		sql = f"SELECT sequence, next FROM code_sequences WHERE state = 'tr' LIMIT {batch_size} OFFSET {batch_size * validation_counter}"

		validation_counter += 1

		c.execute(sql)

		rows = c.fetchall()

		sequences = []
		nexts = []

		for sequence, next in rows:
			temp = []
			for char in sequence:
				temp.append(ord(char))

			sequences.append(temp)
			nexts.append(ord(next))

		x,y =  ont_hot(sequences, nexts, batch_size)

		assert x.shape == (batch_size, 40), "Invalid dimension for Input X"
		assert y.shape == (batch_size, 128), "Invalid dimension for Output Y"

		yield x, y

def test_generator(batch_size):
	global test_counter

	while True:
		sql = f"SELECT sequence, next FROM code_sequences WHERE state = 'tr' LIMIT {batch_size} OFFSET {batch_size * test_counter}"

		test_counter += 1

		c.execute(sql)

		rows = c.fetchall()

		sequences = []
		nexts = []

		for sequence, next in rows:
			temp = []
			for char in sequence:
				temp.append(ord(char))

			sequences.append(temp)
			nexts.append(ord(next))

		x,y =  ont_hot(sequences, nexts, batch_size)

		assert x.shape == (batch_size, 40), "Invalid dimension for Input X"
		assert y.shape == (batch_size, 128), "Invalid dimension for Output Y"

		yield x, y
