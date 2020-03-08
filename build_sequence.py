"""
	This file generate sequences from the code and saves it into a sqlite file

	@author: Abhishek Chatterjee (imdeepmind)
"""

import sqlite3
import random
from tqdm import tqdm

conn = sqlite3.connect('data/code.db')
c = conn.cursor()

transcations = []

def create_table():
	c.execute("CREATE TABLE IF NOT EXISTS code_sequences(sequence TEXT, next TEXT, state TEXT);")

def transaction_bldr(sql):
	global transcations

	transcations.append(sql)

	if len(transcations) > 1000:
		random.shuffle(transcations)

		c.execute("BEGIN TRANSACTION")

		for transcation in transcations:
			try:
				c.execute(transcation)
			except Exception as ex:
				print('Transaction fail ', ex)
				print('SQL ', transcation)

		c.execute("commit")
		transcations = []

def process_data(data):
	return data.replace("'", "''")

def insert_data(sequence, next, state):
	# print(sequence, next, process_data(sequence), process_data(next))
	sql = f"INSERT INTO code_sequences(sequence, next, state) VALUES('{process_data(sequence)}', '{process_data(next)}', '{state}');"
	transaction_bldr(sql)


with open("data/code_list.txt", "r") as f:
	create_table()

	file = f.read()

	files = file.split("\n")

	for file in tqdm(files):
		try:
			with open(file, 'r') as f:
				code = f.read()

				n = len(code)

				SEQ_LENGTH = 40
				TRAIN_SIZE = int(n * 0.8)
				VALIDATION_SIZE = int(n * 0.1) + TRAIN_SIZE
				TEST_SIZE = int(n * 0.1) + TRAIN_SIZE + VALIDATION_SIZE

				for k in range(n - SEQ_LENGTH):
					seq = code[k:k + SEQ_LENGTH]
					next = code[k + SEQ_LENGTH]

					if k <= TRAIN_SIZE:
						state = "tr"
					elif k <= VALIDATION_SIZE:
						state = "va"
					else:
						state = "te"

					insert_data(seq, next, state)

		except Exception as ex:
			print(ex)