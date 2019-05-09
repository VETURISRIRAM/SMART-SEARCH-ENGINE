"""
@author: Sriram Veturi
@title: SmartSearch - An Intelligent Search Engine.
@date: 05/06/2019
"""

import os

DATA_DIR = "./documents/"


def remove_extra_lines_and_tabs():
	"""
	Funtion to remove extra lines and tabs from documents.
	"""

	for filename in os.listdir(DATA_DIR):

		clean_lines = []
		with open(os.path.join(DATA_DIR, filename), "r") as f:
		    lines = f.readlines()
		    clean_lines = [l.strip() for l in lines if l.strip()]

		with open(os.path.join(DATA_DIR, filename), "w") as f:
		    f.writelines('\n'.join(clean_lines))
