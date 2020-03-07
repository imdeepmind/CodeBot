from os import listdir
from os.path import isfile, join
import random

files = []

def is_file(path, file):
	return isfile(join(path, file))

def return_files_and_folders(path):
	# To limit the no of prints, to make the process fast
	if random.randint(0,100) == 50:
		print(f'--Processing file {path}--')

	files = []
	folders = []
	directories = listdir(path)

	for directory in directories:
		file = is_file(path, directory)

		if file:
			files.append(join(path, directory))
		else:
			folders.append(join(path, directory))

	return files, folders

def process_files(path):
	global files

	_files, _folders = return_files_and_folders(path)

	files = files + _files

	for folder in _folders:
		process_files(folder)

def filter_files():
	filtered_files = []
	extensions = ['c', 'h', 'cpp', 'cc', 'c++', 'cp', 'cxx', 'ii', 'cxx']

	for file in files:
		extension = file.split('/')[-1].split('.')[-1]

		if extension in extensions:
			filtered_files.append(file)

	return filtered_files

process_files("data/chromium-master")
filtered_files = filter_files()

with open("data/code_list.txt", 'w') as f:
	f.write("\n".join(filtered_files))