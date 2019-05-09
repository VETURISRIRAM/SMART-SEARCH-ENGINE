import os
import json
import time
import argparse
import operator

from cosine_similarity import get_top_200_similar_urls

# Globals..
QUERIES_DIR = "./sample_queries"
RANKS_DIR = "./web_page_ranks"


def get_top_ten_sites(user_query):
	"""
	Function to display the top ten sites based on user's query.
	:return top_ten_urls_dict: Top ten links based on user's query.
	"""

	# Dictionary to store the most relevant (Top 10) urls.
	top_ten_urls_dict = dict()

	# Just a simple query defined by me.
	warmup_query = "UIC Computer Science Grad School.\n"

	# Make sure to end the query by a period.
	# Query separation code used period to differentiate between different queries.

	# user_query = str(list(user_query.keys())[0])
	if user_query[-1] != ".":

		user_query += "."

	with open(os.path.join(QUERIES_DIR, "sample_query_examples"), "w") as qf:

		qf.write(warmup_query)
		qf.write(user_query)

	# Get the Top 200 urls based on Vector Space Model (TF-IDF Scheme.
	top_matched_urls = get_top_200_similar_urls()

	# Now, get the top ranked urls based on web page ranks saved in "./web_page_ranks/web_ranks.json"
	for query_number, relevant_urls in top_matched_urls.items():

		# To store the top ten urls for each query in sample query examples file.
		individual_query_relevant_urls = dict()

		with open(os.path.join(RANKS_DIR, "web_ranks.json"), "r") as rf:

			ranks_dict = dict(json.load(rf))

			for relevant_url in relevant_urls:

				page_score = ranks_dict[relevant_url]
				individual_query_relevant_urls[relevant_url] = page_score

		# Sort and get only top ten.
		sorted_top_urls = sorted(individual_query_relevant_urls.items(), key=operator.itemgetter(1))
		top_ten_urls_with_score = sorted_top_urls[-9:]

		best_urls_each = list()
		for url_score_map in top_ten_urls_with_score:

			# First index is the website and the second one is the score.
			best_urls_each.append(url_score_map[0])

		# Push it to the main map of top urls.
		top_ten_urls_dict[query_number] = best_urls_each

	return top_ten_urls_dict


def main_search(query):
	"""
	Driver function to perform search operation.
	:return 
	"""

	# Get user's query.
	# user_query = args.query
	user_query = query
	# user_query = "information retrieval" yields a site with Professor Cornelia Caregea's profile who teaches Information Retrieval at UIC

	if user_query == "":

		raise Exception("Please enter a query to get the relevant links.")

	print("##################", user_query)
	# Record the start time.
	retrieval_start_time = time.time()

	# Get the top sites based on user's query.
	top_sites = get_top_ten_sites(user_query)

	# Record the end time.
	retrieval_end_time = time.time()


	# First Query is a test query.
	# Second Query is the user query.
	# print(top_sites)
	user_query_urls = top_sites[2]

	# Printing out the links.
	print("####################################################")
	print("Here are the links based on your query.")
	print("####################################################")

	ui_output = "\n".join(user_query_urls)

	for link in user_query_urls:
		print(link)
		print()

	print("Time taken to retrieve relevant sites based on your query : {} Seconds.".format((retrieval_end_time - retrieval_start_time)))

	return user_query_urls
