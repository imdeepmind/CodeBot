import random
import sqlite3
import numpy as np
import tensorflow as tf
import tensorflow.keras as keras

from os import listdir
from os.path import isfile, join
from tqdm import tqdm
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense

class Model:
	__files = []
	__transcations = []
	__train_counter = 0
	__validation_counter = 0
	__test_counter = 0

	def __is_file(self, path, file):
		"""
			Check if a partucular file exists in the particular path

			Args:
				path: path of the folder
				file: filename
		"""
		return isfile(join(path, file))

	def __is_code_list_available(self):
		"""
			Check of Code File List is available or not

			Args:

		"""
		return self.__is_file(self.DATA_FOLDER, self.CODE_FILE_LIST)

	def __is_sequences_db_available(self):
		"""
			Check of sequence db file is available or not

			Args:

		"""
		return self.__is_file(self.DATA_FOLDER, self.SEQUENCE_DB)

	def __return_files_and_folders(self, path):
		"""
			Returns all the files and folders present on a specific path

			Args:
				path: path name

		"""
		if random.randint(0,100) == 50:
			print(f'Processing file {path}')

		files = []
		folders = []
		directories = listdir(path)

		for directory in directories:
			file = self.__is_file(path, directory)

			if file:
				files.append(join(path, directory))
			else:
				folders.append(join(path, directory))

		return files, folders

	def __extract_files(self, path):
		"""
			Extracts every files present on the codebase

			Args: 
				path: path name
	
		"""
		_files, _folders = self.__return_files_and_folders(path)

		self.__files += _files

		for folder in _folders:
			self.__extract_files(folder)

	def __filter_files(self):
		"""
			Filter all files and extracts only the c/c++ codes

			Args:

		"""
		filtered_files = []
		extensions = ['c', 'h', 'cpp', 'cc', 'c++', 'cp', 'cxx', 'ii', 'cxx']

		for file in self.__files:
			extension = file.split('/')[-1].split('.')[-1]

			if extension in extensions:
				filtered_files.append(file)

		return filtered_files

	def __generate_code_list_file(self):
		"""
			Generates list of code files and then filters only the c/c++ code files, And finally saves it in a seperate txt file

			Args:

		"""
		self.__extract_files(self.DATA_FOLDER + "/chromium-master")
		
		filtered_files = self.__filter_files()

		with open(self.DATA_FOLDER + "/" + self.CODE_FILE_LIST, 'w') as f:
			f.write("\n".join(filtered_files))

	def __create_table(self, c):
		"""
			Creates a table for storing the data

			Args:
				c: cursor to the sqlite
		"""
		c.execute("CREATE TABLE IF NOT EXISTS code_sequences(sequence TEXT, next TEXT, state TEXT);")

	def __transaction_bldr(self, sql, c):
		"""
			Transcation builder that stores the data in a batch

			Args:
				sql: sql query to add data
				c: cursor to the sqlite 
		"""
		self.__transcations.append(sql)

		if len(self.__transcations) > 1000:
			random.shuffle(self.__transcations)

			c.execute("BEGIN TRANSACTION")

			for transcation in self.__transcations:
				try:
					c.execute(transcation)
				except Exception as ex:
					print('Transaction fail ', ex)
					print('SQL ', transcation)

			c.execute("commit")
			self.__transcations = []

	def __process_data(self, data):
		"""
			Process data for inserting into db

			Args:
				data: data that needed to be process
		"""
		return data.replace("'", "''")

	def __insert_data(self, sequence, next, state, c):
		"""
			Builds SQL query to save data into db

			Args:
				sequence: sequence to save into db
				next: next character after the sequence
				state: state of the data (trainining/validation/test data)
				c: cursor to the sqlite db

		"""
		sql = f"INSERT INTO code_sequences(sequence, next, state) VALUES('{self.__process_data(sequence)}', '{self.__process_data(next)}', '{state}');"
		
		self.__transaction_bldr(sql, c)

	def __build_sequence_db(self):
		"""
			Building sequences to store into the db

			Args:

		"""
		with open(self.DATA_FOLDER + "/" + self.CODE_FILE_LIST, "r") as f:
			conn = sqlite3.connect(self.DATA_FOLDER + "/" + self.SEQUENCE_DB)
			c = conn.cursor()

			self.__create_table(c)

			file = f.read()

			files = file.split("\n")

			for file in tqdm(files):
				try:
					with open(file, 'r') as f:
						code = f.read()

						n = len(code)

						TRAIN_SIZE = int(n * 0.8)
						VALIDATION_SIZE = int(n * 0.1) + TRAIN_SIZE
						TEST_SIZE = int(n * 0.1) + TRAIN_SIZE + VALIDATION_SIZE

						for k in range(n - self.SEQ_LENGTH):
							seq = code[k:k + self.SEQ_LENGTH]
							next = code[k + self.SEQ_LENGTH]

							if k <= TRAIN_SIZE:
								state = "tr"
							elif k <= VALIDATION_SIZE:
								state = "va"
							else:
								state = "te"

							self.__insert_data(seq, next, state, c)

				except Exception as ex:
					print(ex)
		
	def __one_hot(self, sequences, nexts):
		"""
			One Hot Encoding for the labels and coverts everything into numpy array

			Args:
				sequences: a batch of sequences
				nexts: a batch of next characters

		"""
		y = np.zeros((self.BATCH_SIZE, 128), dtype=np.bool)

		for i, sequence in enumerate(sequences):
			if nexts[i] < 0 or nexts[i] > 128:
				y[i, 97] = 1
			else:
				y[i, nexts[i]] = 1

		return np.array(sequences), y

	def __train_generator(self):
		"""
			Train Generator that generates a batch of data for the model

			Args:

		"""
		while True:
			conn = sqlite3.connect(self.DATA_FOLDER + "/" + self.SEQUENCE_DB)
			c = conn.cursor()

			sql = f"SELECT sequence, next FROM code_sequences WHERE state = 'tr' LIMIT {self.BATCH_SIZE} OFFSET {self.BATCH_SIZE * self.__train_counter}"

			self.__train_counter += 1

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

			x,y =  self.__one_hot(sequences, nexts)

			assert x.shape == (self.BATCH_SIZE, 40), "Invalid dimension for Input X"
			assert y.shape == (self.BATCH_SIZE, 128), "Invalid dimension for Output Y"

			yield  x, y

	def __validation_generator(self):
		"""
			Validation Generator that generates a batch of data for the model

			Args:
			
		"""
		while True:
			conn = sqlite3.connect(self.DATA_FOLDER + "/" + self.SEQUENCE_DB)
			c = conn.cursor()

			sql = f"SELECT sequence, next FROM code_sequences WHERE state = 'va' LIMIT {self.BATCH_SIZE} OFFSET {self.BATCH_SIZE * self.__validation_counter}"

			self.__validation_counter += 1

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

			x,y =  self.__one_hot(sequences, nexts)

			assert x.shape == (self.BATCH_SIZE, 40), "Invalid dimension for Input X"
			assert y.shape == (self.BATCH_SIZE, 128), "Invalid dimension for Output Y"

			yield  x, y

	def __test_generator(self):
		"""
			Test Generator that generates a batch of data for the model

			Args:
			
		"""
		while True:
			conn = sqlite3.connect(self.DATA_FOLDER + "/" + self.SEQUENCE_DB)
			c = conn.cursor()

			sql = f"SELECT sequence, next FROM code_sequences WHERE state = 'te' LIMIT {self.BATCH_SIZE} OFFSET {self.BATCH_SIZE * self.__test_counter}"

			self.__test_counter += 1

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

			x,y =  self.__one_hot(sequences, nexts)

			assert x.shape == (self.BATCH_SIZE, 40), "Invalid dimension for Input X"
			assert y.shape == (self.BATCH_SIZE, 128), "Invalid dimension for Output Y"

			yield  x, y

	def generate_code_list(self, force=False):
		"""
			Generating a code list file

			Args:
				force: Forcefully generating a code list file
		"""
		if force:
			print("Generating code list file...")

			# Generating a code list file
			self.__generate_code_list_file()

			return
		else:
			# Check of code list file available?
			code_list_available = self.__is_code_list_available()

			if not code_list_available:
				print("Generating code list file...")

				# If there is no code list file, then generates a new code list file
				self.__generate_code_list_file()
			else:
				print("Found existing code list file...")

	def build_sequences(self, force):
		"""
			Method for generating sequences of text with the next character and storing it into sqlite db

			Args:

		"""
		if force:
			print("Generating sequences...")

			# Generating sequecne db
			self.__build_sequence_db()
		else:
			if self.__is_sequences_db_available():
				print("Found existing sequence db file...")
			else:
				print("Generating sequences...")

				# Generating sequecne db
				self.__build_sequence_db()

	def build_model(self):
		train_g = self.__train_generator()
		validation_g = self.__validation_generator()
		test_g = self.__test_generator()

		model = Sequential()
		model.add(Embedding(self.VOCAB_SIZE, 128, input_length=self.SEQ_LENGTH))
		model.add(LSTM(128))
		model.add(Dense(128, activation='softmax'))

		model.compile(loss="categorical_crossentropy", optimizer='adam', metrics=['accuracy'])

		print(model.summary())

		model.fit_generator(train_g, 
							steps_per_epoch=self.STEPS_PER_EPOCH,
							epochs=self.EPOCHS,
							validation_data=validation_g,
		                    validation_steps=self.STEPS_PER_EPOCH_VALIDATION)

	def __init__(self, 
				DATA_FOLDER='data',
				CODE_FILE_LIST='code_list.txt', 
				SEQUENCE_DB="sequeces.db",
				SEQ_LENGTH=40,
				BATCH_SIZE=32,
				VOCAB_SIZE=128,
				STEPS_PER_EPOCH=None,
				STEPS_PER_EPOCH_VALIDATION=None,
				TRAIN_SIZE = 33274973,
				VALIDATION_SIZE = 4150122,
				TEST_SIZE = 3870306,
				EPOCHS=5
				):

		# All the constants for the project
		self.DATA_FOLDER = DATA_FOLDER
		self.CODE_FILE_LIST = CODE_FILE_LIST
		self.SEQUENCE_DB = SEQUENCE_DB
		self.SEQ_LENGTH = SEQ_LENGTH
		self.BATCH_SIZE = BATCH_SIZE
		self.VOCAB_SIZE = VOCAB_SIZE
		self.TRAIN_SIZE = TRAIN_SIZE
		self.VALIDATION_SIZE = VALIDATION_SIZE
		self.TEST_SIZE = TEST_SIZE,
		self.EPOCHS = EPOCHS

		if STEPS_PER_EPOCH:
			self.STEPS_PER_EPOCH = STEPS_PER_EPOCH
		else:
			self.STEPS_PER_EPOCH = self.TRAIN_SIZE // self.BATCH_SIZE

		if STEPS_PER_EPOCH_VALIDATION:
			self.STEPS_PER_EPOCH_VALIDATION = STEPS_PER_EPOCH_VALIDATION
		else:
			self.STEPS_PER_EPOCH_VALIDATION = self.VALIDATION_SIZE // self.BATCH_SIZE