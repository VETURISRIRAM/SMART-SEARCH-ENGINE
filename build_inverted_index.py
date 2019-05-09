"""
@author: Sriram Veturi
@title: SmartSearch - An Intelligent Search Engine.
@date: 05/06/2019
"""

import os
import math
import json

DATA_DIR = "./documents"
TF_IDF_FILES_DIR = "./tf_idf_files"


def generate_tf():
	"""
	Function to build the corpus for every document.
	:return tf_dict: Ter Frequency Dictionary (Mapping of documents with term frequencies of words in it).
	"""

	# Dictionary to store term frequency of each term in each url.
	tf_dict = dict()

	i = 0

	# Traverse through the 'documents' directory and get words for each url.
	for json_file in os.listdir(DATA_DIR):
		
		# Open the file and contents.
		with open(os.path.join(DATA_DIR, json_file), "r") as jf:

			# To store term frequency of words in each url.
			tf_dict_each = dict()

			# Load the dictionary
			url_text_dict = dict(json.load(jf))
			url_word_count_map = url_text_dict["WORD_COUNT_MAP"]

			# "url_word_count_map" is dictionary with word and its frequency.
			total_words = sum(list(url_word_count_map.values()))

			for word, word_count in url_word_count_map.items():

				tf_dict_each[word] = word_count / total_words

			# Push individual tf_dict_each to main tf_dict
			tf_dict[url_text_dict["URL"]] = tf_dict_each

	return tf_dict


def generate_idf():
	"""
	Function to generate the inverse document frequency.
	:return idf_dict: Inverse Document Frequency Mapping.
	"""

	# Total number of json files in the data directory.
	total_pages = len(os.listdir(DATA_DIR))

	# Dicitonary to store the IDF of each document.
	idf_dict = dict()

	#######################
	# GENARATE VOCABULARY #
	#######################

	# Vocabulary of all the words in all the urls.
	all_words_in_all_urls = list()
	i = 0
	# Traverse through the 'documents' directory and get words for each url.
	for json_file in os.listdir(DATA_DIR):
		if i >= 200:
			break
		i += 1
		
		# Open the file and contents.
		with open(os.path.join(DATA_DIR, json_file), "r") as jf:

			# To store term frequency of words in each url.
			tf_dict_each = dict()

			# Load the dictionary
			url_text_dict = dict(json.load(jf))

			# Get all the words in this particular document/url.
			all_words_in_this_url = list(url_text_dict["WORD_COUNT_MAP"].keys())

			# Append it to main list
			all_words_in_all_urls += all_words_in_this_url

	# Vocabulary of all urls.
	vocabulary = set(all_words_in_all_urls)

	print(len(vocabulary))
	#################
	# IDF OPERATION #
	#################
	j = 0
	for word in vocabulary:

		print(j)
		j += 1

		# To track how many urls have this word of vocabulary.
		word_count = 0

		# Traverse through the 'documents' directory and get words for each url.
		for json_file in os.listdir(DATA_DIR):
			
			# Open the file and contents.
			with open(os.path.join(DATA_DIR, json_file), "r") as jf:

				# To store term frequency of words in each url.
				tf_dict_each = dict()

				# Load the dictionary
				url_text_dict = dict(json.load(jf))

				# Get all the words in this particular document/url.
				all_words_in_this_url = list(url_text_dict["WORD_COUNT_MAP"].keys())

				if word in all_words_in_this_url:

					word_count += 1

		# Now, we know how many urls contain the word.
		# Let's calculate idf.
		if word_count == 0:

			continue

		else:

			idf_dict[word] = math.log(total_pages / word_count)

	return idf_dict


def generate_tf_idf(tf_dict, idf_dict):
	"""
	Function to generate TF-IDF.
	:return tf_idf_dict: TF-IDF Mapping.
	"""

	# To store TF-IDF dictionary.
	tf_idf_dict = dict()

	# Traverse through the 'documents' directory and get words for each url.
	for json_file in os.listdir(DATA_DIR):
		print(json_file)
		
		# Open the file and contents.
		with open(os.path.join(DATA_DIR, json_file), "r") as jf:

			# To store term frequency of words in each url.
			tf_dict_each = dict()

			# Load the dictionary
			url_text_dict = dict(json.load(jf))

			# Get all the words in this particular document/url.
			all_words_in_this_url = list(url_text_dict["WORD_COUNT_MAP"].keys())
			this_url = url_text_dict["URL"]
			tf_idf_dict_each = dict()

			# Product of TF and IDF here.
			for word in all_words_in_this_url:
				try:

					tf_idf_dict_each[word] = tf_dict[this_url][word] * idf_dict[word]
				except:

					continue

		tf_idf_dict[this_url] = tf_idf_dict_each

	return tf_idf_dict


def create_directory():
	"""
	Function to create a directory to store the documents.
	:return True/False: Creation Successful Flag.
	"""

	# If it already exists, return True.
	if os.path.isdir(TF_IDF_FILES_DIR) is True:

		print("Directory to store the tf-idf already exists. Moving on.")
		return True

	else:

		try:
			
			os.mkdir(TF_IDF_FILES_DIR)
			print("Directory created to store the tf-idf files.")
			return True

		except Exception as e:

			print(e)
			return False


def create_vector_space_model():
	"""
	Driver funciton to generate TF-IDF files for further use.
	"""

	# Check if directory already exists.
	# If no, create one.
	if create_directory() is True:

		# Generate Term Frequency and save json.
		tf_dict = generate_tf()
		with open(os.path.join(TF_IDF_FILES_DIR, 'tf.json'), 'w') as fp:

		    json.dump(tf_dict, fp)


		# Generate Inverse Document Frequency and save json.
		idf_dict = generate_idf()
		with open(os.path.join(TF_IDF_FILES_DIR, 'idf.json'), 'w') as fp:

		    json.dump(idf_dict, fp)


		# Generate TF-IDF and save json.
		tf_idf_dict = generate_tf_idf(tf_dict, idf_dict)
		with open(os.path.join(TF_IDF_FILES_DIR, 'tf_idf.json'), 'w') as fp:

		    json.dump(tf_idf_dict, fp)

	else:

		raise Exception("DirectoryCreationError: Could not create directory to store TF-IDF related files.")


create_vector_space_model()
