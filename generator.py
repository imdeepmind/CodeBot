import sqlite3
import numpy as np

train_couter = 0

conn = sqlite3.connect('data/code.db')
c = conn.cursor()

def ont_hot(sequences, nexts, batch_size):
    x = np.zeros((batch_size, 40, 128), dtype=np.bool)
    y = np.zeros((batch_size, 128), dtype=np.bool)

    for i, sequence in enumerate(sequences):
    	for t, char in enumerate(sequence):
    		if char < 0 or char > 128:
    			char = 97
    		x[i, t, char] = 1

    	if nexts[i] < 0 or nexts[i] > 128:
    		y[i, 97] = 1
    	else:
    		y[i, nexts[i]] = 1

    return x, y

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

		print(sequences, nexts)

		yield ont_hot(sequences, nexts, batch_size)
