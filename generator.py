import sqlite3

train_couter = 0

conn = sqlite3.connect('data/code.db')
c = conn.cursor()

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

		yield sequences, nexts
