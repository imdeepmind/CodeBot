from os import listdir
from os.path import isfile, join
import random

class Model:
	__files = []

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

	def __init__(self, 
				DATA_FOLDER='data',
				CODE_FILE_LIST='code_list.txt'):

		# All the constants for the project
		self.DATA_FOLDER = DATA_FOLDER
		self.CODE_FILE_LIST = CODE_FILE_LIST


		