"""
@author: Sriram Veturi
@title: SmartSearch - An Intelligent Search Engine.
@date: 05/06/2019
"""

import re
import urllib
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from http.cookiejar import CookieJar
from nltk.tokenize import word_tokenize


def extract_text_from_page(url):
	"""
	Function to extract text data from the webpage.
	:param url: Webpage from which text is to be extracted.
	:return text_data: Extracted text.
	"""

	# Source: https://stackoverflow.com/questions/328356/extracting-text-from-html-file-using-python
	# Source: https://stackoverflow.com/questions/32569934/urlopen-returning-redirect-error-for-valid-links
	# Adding a Cookie Jar to avoid the redirect the request and get into an infinite loop.
	url_request = urllib.request.Request(url, None, {'User-Agent': "Some-Random-User"})

	# Cookie Jar Object.
	cj = CookieJar()
	opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
	response = opener.open(url_request)
	raw_response = response.read().decode('utf8', errors='ignore')
	soup = BeautifulSoup(raw_response, "lxml")

	# Kill all script and style elements.
	for script in soup(['style', 'script', 'head', 'title', 'meta', '[document]']):
		script.extract()

	# get text
	text = soup.get_text()

	# Break into lines and remove leading and trailing space on each.
	lines = (line.strip() for line in text.splitlines())

	# Break multi-headlines into a line each.
	chunks = (phrase.strip() for line in lines for phrase in line.split("  "))

	# Drop blank lines.
	text_data = ' '.join(chunk for chunk in chunks if chunk)

	return text_data


def preprocess_text(text_data):
	"""
	Function to preprocess the text data.
	:param text_data: Text to be preprocessed.
	:return corpus: Preprocessed text.
	"""

	# Some initializations.
	stopWords = set(stopwords.words("english"))
	ps = PorterStemmer()

	# Tokenize text contents
	contents = word_tokenize(text_data)

	# To store the corpus of words
	corpus = list()

	# Create corpus, remove special chars and lowercase operation.
	for content in contents:

		content = re.sub('[^A-Za-z]+', '', content).lower()
		corpus.append(content)

	# Remove Stopwords before stemming
	corpus = [word for word in corpus if word not in stopWords]

	# Integrate Porter Stemmer
	corpus = [ps.stem(word) for word in corpus]

	# Remove Stopwords after stemming
	corpus = [word for word in corpus if word not in stopWords]

	# Remove unnecessary empty strings from corpus
	corpus = [word for word in corpus if word != '' and len(word) > 2]

	# Convert back to string
	corpus = " ".join(corpus)

	return corpus
