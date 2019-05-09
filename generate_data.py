"""
@author: Sriram Veturi
@title: SmartSearch - An Intelligent Search Engine.
@date: 05/06/2019
"""

import os
import json
import collections

from clean_html import extract_text_from_page
from clean_html import preprocess_text

DATA_DIRECTORY = "./documents"


def create_data_directory():
	"""
	Function to create a directory to store the documents.
	:return True/False: Creation Successful Flag.
	"""

	# If it already exists, return True.
	if os.path.isdir(DATA_DIRECTORY) is True:

		print("Directory to store the documents already exists. Moving on.")
		return True

	else:

		try:
			
			os.mkdir(DATA_DIRECTORY)
			print("Directory created to store the documents.")
			return True

		except Exception as e:

			print(e)
			return False


def create_documents(sites_list, parent_children_url_map):
	"""
	Function to create documents in the directory.
	:param sites_list: The list of sites crawled.
	"""

	# Index to store the document name.
	document_name_index = 1

	try:

		# Traverse through the urls, preprocess them and create document.
		for page_url in sites_list:

			try:

				print("Processing document {doc_number}.".format(doc_number=document_name_index))
				raw_text_data = extract_text_from_page(page_url)
				preprocessed_text = preprocess_text(raw_text_data)
				preprocessed_text_words = preprocessed_text.split(" ")
				preprocessed_text_words_count_map = dict(collections.Counter(preprocessed_text_words))

				document_contents_map = dict()
				document_contents_map["INDEX"] = document_name_index
				document_contents_map["URL"] = page_url

				# Some urls in the parent_children_url_map would not have children.
				try: 

					document_contents_map["OUTGOING_LINKS"] = parent_children_url_map[page_url]

				except:

					# If no children, empty list as all outgoing urls list.
					document_contents_map["OUTGOING_LINKS"] = []

				document_contents_map["WORD_COUNT_MAP"] = preprocessed_text_words_count_map

				# Create a json file which would store the web graph information of the url.
				document_name = str(document_name_index) + ".json"
				with open(os.path.join(DATA_DIRECTORY, document_name), 'w') as doc_file:

					json.dump(document_contents_map, doc_file)

				document_name_index += 1

			except Exception as e:

				print("Could not extract text from {url} because of the error below.\n".format(url=page_url))
				print(e)
				continue

		return True

	except Exception as e:

		print(e)
		return False
