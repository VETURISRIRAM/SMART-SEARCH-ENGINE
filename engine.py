"""
@author: Sriram Veturi
@title: SmartSearch - An Intelligent Search Engine.
@date: 05/06/2019
"""

import time
import argparse

from crawl_all_sites import crawl_for_sites
from generate_data import create_documents
from generate_data import create_data_directory
from clean_documents import remove_extra_lines_and_tabs

# Parse Arguments
parser = argparse.ArgumentParser(description="Crawler for Search Engine")
parser.add_argument(
    "--initial_url", 
    type=str,
    help="The initial URL to start the crawling process from. For example: 'https://www.cs.uic.edu/'"
)
parser.add_argument(
    "--number_of_pages", 
    type=int,
    help="The number of pages to crawl and create database from."
)
parser.add_argument(
    "--domain", 
    type=str,
    help="The domain in which crawling should happen. For example: 'uic.edu'"
)
args = parser.parse_args()


def crawler_driving_function():
	"""
	Driver Function to crawl for sites and create database.
	"""

	# Time to record the start time of the program execution.
	db_creation_start_time = time.time()

	# Time to record the start time of the crawling.
	crawl_start_time = time.time()

	print("################################################################################################")

	print("Web Crawling startes now.\n\n")

	# Initialize the user arguments.
	main_url = args.initial_url
	min_pages_to_crawl = args.number_of_pages
	domain = args.domain

	# Get the crawled sites and unknown sites.
	sites_list, unknown_urls, broken_urls, parent_children_url_map = crawl_for_sites(main_url, min_pages_to_crawl, domain)

	# Record crawl end time.
	crawl_end_time = time.time()
	print("\n\nWeb Crawling finished now.\n")

	print("################################################################################################")

	print("Total time to crawl the web: {} Minutes".format((crawl_end_time - crawl_start_time)/60))

	# Check if there are any duplicate pages in the list.
	if len(sites_list) == len(list(set(sites_list))):

		print("No duplicate sites included.")

	else:

		print("Duplicates found. Removing Duplicates.")
		sites_list = list(set(sites_list))

	print("################################################################################################")

	print("Now, extracting the text data from the crawled websites.")

	print("################################################################################################")

	if create_data_directory():

		print("################################################################################################\n\n")

		creation_flag = create_documents(sites_list, parent_children_url_map)
		print("\n\nText extracted from the crawled pages.")

	else:

		raise Exception("DirectoryError: You do not have write privilege in the directory.")

	print("################################################################################################")

	print("Total time to create the database: {db_creation_time} Minutes.".format(db_creation_time=(time.time() - db_creation_start_time) / 60))

	print("################################################################################################")

	print("Unknown Achors Found:\n")
	print(unknown_urls)

	print("################################################################################################")

	if broken_urls != []:

		print("Broken / Unreachable URLs Found:\n")
		print(broken_urls)

		print("################################################################################################")

# Main funciton starts here..
if __name__ == "__main__":

	crawler_driving_function()
