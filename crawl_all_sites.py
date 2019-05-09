"""
@author: Sriram Veturi
@title: SmartSearch - An Intelligent Search Engine.
@date: 05/06/2019
"""

import requests
from uuid import uuid4
from bs4 import BeautifulSoup
from urllib.parse import urlsplit

DOMAIN = "uic.edu"


def check_goodness(url):
    """
    Function to check if the url is a dead end (pds, doc, docx, etc)
    :param url: Link to be checked.
    :return True/False: Flag if dead end or not.
    """

    # Documents are not necessary.
    unnecessary_extensions = [
        '.pdf',
        '.doc',
        '.docx',
        '.xls',
        '.avi', 
        '.mp4',
        '.xlsx',
        '.jpg',
        '.png',
        '.gif', 
        '.pdf', 
        '.gz', 
        '.rar', 
        '.tar', 
        '.rv',
        '.tgz', 
        '.zip', 
        '.exe', 
        '.js', 
        '.css', 
        '.ppt'        
    ]
    for extension in unnecessary_extensions:

        if extension in url:

            return False

    # Sometimes, the urls contain '@' to indicate a phone number or email address.
    # Remove such urls.
    if '@' in url:

        return False

    # If everything is alright, return True.
    return True

def check_domain(url, main_domain):
    """
    Function to check the crawling is limited to UIC domain.
    :param url: URL to check.
    :return True/False: Flag to indicate whether the site is in the domain.
    """

    # If domain is not specified, return true.
    if main_domain == "":

    	return True

    if main_domain in url:

        return True

    else:

        return False


def crawl_for_sites(main_url, number_of_pages_to_crawl, main_domain):
    """
    Funtion to initialize the queue to store all the websites.
    :param main_url: Initial point to start crawling.
    :param number_of_pages_to_crawl: Minimum number of pages to crawl.
    :param main_domain: The domain to stick with while crawling.
    :return sites: List of websites.
    """

    # List to store crawled sites and Queue for BFS.
    sites_list = list()
    helper_queue = list()
    unknown_urls = list()
    broken_urls = list()

    # Map to store the document and words in the document.
    documents_words_count_map = dict()

    # Mao to store the outgoing urls from the parent url.
    parent_children_url_map = dict()

    # Check if main url is responding with a 200 OK.
    try:

    	# Minor preprocessing.
        # Remove "www." from the main url
        main_url = main_url.replace("www.", "")

        # Generating a random user agent as client
        # So, even though many requests are sent, it is not considered as spamming.
        # Basically, IP Spoofing.
        main_url_response = requests.get(
            main_url,
            headers = {'User-agent': 'Some-Anonymous-User-{}'.format(str(uuid4()))}
        )

        # If the main url can not be crawled, raise exception.
        if main_url_response.status_code != 200:

            raise Exception('\nThe main URL ({url}) can not be reached.\n'.format(url=main_url))
            broken_urls.append(main_url)

    # The main url could be broken.
    except:

        raise Exception('\nThe main URL ({url}) provided is broken.\n'.format(url=main_url))
        broken_urls.append(main_url)

    # Add the main url to our queue and sites list.
    sites_list.append(main_url)
    helper_queue.append(main_url)

    # Index of number of crawled websites.
    crawled_sites_number = 0

    # Operation to crawl only 3000 sites
    while crawled_sites_number < number_of_pages_to_crawl or not helper_queue:

        # Store the local outgoing urls.
        local_urls = list()

        # Pop the url to crawl.
        url = helper_queue.pop()

        # Minor preprocessing.
        # Remove "www." from the main url
        url = url.replace("www.", "")

        # Extract base url to resolve relative links.
        # Source: https://medium.freecodecamp.org/how-to-build-a-url-crawler-to-map-a-website-using-python-6a287be1da11.
        url_parts = urlsplit(url)
        url_base = (url_parts.netloc).replace("www.", "")
        url_base = url_parts.scheme + "://" + url_parts.netloc

        # If URL = "https://somewebsite.com/something",
        # then path should only be "https://somewebsite.com/"
        if '/' in url:
            url_path = url[:url.rfind('/') + 1]
        else:
            url_path = url

        # Hit the site.
        try:

            # Generating a random user agent as client
            # So, even though many requests are sent, it is not considered as spamming.
            # Basically, IP Spoofing.
            url_response = requests.get(
                url,
                headers = {'User-agent': 'Some-Anonymous-User-{}'.format(uuid4())}
            )

            # Continue if the site is unresponsive.
            if url_response.status_code != 200:

                print("\nThe URL ({url}) is unresponsive. Moving on with next site.\n".format(url=url))
                broken_urls.append(url)
                continue

        # Continue if the site url is broken.
        except Exception as e:
            
            print("\nThe URL ({url}) is broken. Moving on with next site.".format(url=url))
            print("Error: {error_description}".format(error_description=e))
            broken_urls.append(url)
            continue

        # Get the soup of the site.
        site_soup = BeautifulSoup(url_response.text, "lxml")

        # Get all link in the url.
        all_outgoing_links = site_soup.find_all('a')

        # If dead end (no outgoing links), continue.
        if not all_outgoing_links:

            continue

        # Fill the queue with the outgoing links now.
        for link in all_outgoing_links:

            anchor = link.attrs["href"] if "href" in link.attrs else ''

            # Get the fragment and append to the base.
            if anchor.startswith('/') or anchor.startswith("#"):

                local_link = url_base + anchor
                if check_domain(local_link, main_domain):

                    local_urls.append(local_link)

            # If the base is already there, append it.
            elif url_base in anchor:

                # Check the domain so no foreign urls are considered.
                if check_domain(anchor, main_domain):

                    local_urls.append(anchor)

            # If the anchor starts with "http", add it to local urls.
            elif anchor.startswith("http"):

            	# Check the domain so no foreign urls are considered.
                if check_domain(anchor, main_domain):

                    local_urls.append(anchor)

            # If all above conditions fail, it might be an unknown URL.
            else:

            	unknown_urls.append(anchor)

        # Push the url and all the outgoing urls to the document 
        parent_children_url_map[url] = local_urls

        # Add the outgoing urls to the queue from left.
        # Adding from left obeys BFS traversal.
        helper_queue = local_urls + helper_queue
        for l in local_urls:

        	# Check if the URL follows the "GOODNESS" rules mentioned above.
            if check_goodness(l) is False:

                continue

            # To avoid duplicated, check if it is already present in the queue.
            if l not in sites_list:

                print("Crawled Page Information -> Number {number} and URL {site}".format(
                	number=crawled_sites_number, 
                	site=l)
                )
                crawled_sites_number += 1
                sites_list.append(l)

    return sites_list, unknown_urls, broken_urls, parent_children_url_map
