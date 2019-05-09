"""
@author: Sriram Veturi
@title: SmartSearch - An Intelligent Search Engine.
@date: 05/06/2019
"""

import os
import json

from page_rank import get_page_ranks

GRAPH_DIR = "./web_graph"
DATA_DIR = "./documents"
PAGE_RANKS_DIR = "./web_page_ranks"


def build_web_graph():
	"""
	Funciton to build the web graph.
	:return web_graph
	"""

	# First, build a dictionary with URLs and their outgoing links.
	web_graph = dict()

	for json_file_name in os.listdir(DATA_DIR):

		with open(os.path.join(DATA_DIR, json_file_name), "r") as jf:

			# Load JSON as dictionary.
			url_data_dict = dict(json.load(jf))

			# Get URLs and outgoing links.
			url = url_data_dict["URL"]
			outgoing_links = url_data_dict["OUTGOING_LINKS"]

			# Add node to web_graph
			web_graph[url] = outgoing_links

	return web_graph


def get_web_page_ranks():
	"""
	Function to get the page ranks in the entire crawled web.
	:return web_page_rank: Mapping of pages with their page rank scores.
	"""

	# Create directory to store the ranks.
	# If it already exists, return True.
	if os.path.isdir(PAGE_RANKS_DIR) is True:

		print("Directory to store the ranks already exists. Moving on.")

	else:

		try:
			
			os.mkdir(PAGE_RANKS_DIR)
			print("Directory created to store the ranks.")

		except Exception as e:

			print(e)

	# First, build the web graph.
	web_graph = build_web_graph()
	print("Web Graph Built.")
	
	# Now that we have the web graph, get page ranks of all the nodes in the web graph.
	web_page_ranks = get_page_ranks(web_graph)
	print("Ranks calculated.")

	# Create a json file which would store the web graph information of the url.
	document_name = "web_ranks.json"
	with open(os.path.join(PAGE_RANKS_DIR, document_name), 'w') as ranks_file:

		json.dump(web_page_ranks, ranks_file)

	return None

get_web_page_ranks()
