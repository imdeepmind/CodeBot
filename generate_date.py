"""
	This file opens every single code c/c++ file for the chromium project and stores in one file

	@author: Abhishek Chatterjee (imdeepmind)
"""

from tqdm import tqdm

complete_code = ""

with open("data/code_list.txt", "r") as f:
	file = f.read()

	files = file.split("\n")

	for file in tqdm(files):
		try:
			with open(file, 'r') as f:
				complete_code += f.read()
		except Exception as ex:
			print(ex)


with open("data/complete_code.txt", "w") as f:
	f.write(complete_code)
