"""
@author: Sriram Veturi
@title: SmartSearch - An Intelligent Search Engine.
@date: 05/06/2019
"""

import re
import math
import nltk
from pathlib import Path

QUERIES_PATH = "./sample_queries/sample_query_examples"


def generate_TF(corpus, corpus_dict):
    """
    Function to generate TF for queries.
    :param corpus: Corpus of words in the queries.
    :param corpus_dict: Mapping of query number and its corpus.
    :return tf_dict: Term Frequency Mapping.
    """

    tf_dict = dict()
    for document_number, words_in_it in corpus_dict.items():

        tf_dict_each = dict()
        for doc_word in words_in_it:

            tf_dict_each[doc_word] = words_in_it.count(doc_word) / len(words_in_it)

        tf_dict[document_number] = tf_dict_each

    return tf_dict


def generate_IDF(corpus, corpus_dict, total_queries):
    """
    Function to generate IDF for all the words in the vocab.
    :param corpus: Corpus of words in the queries.
    :param corpus_dict: Mapping of query number and its corpus.
    :param total_queries: Total number of queries.
    :return idf_dict: Inverse Document Frequency Mapping.
    """

    # Compute the number of documents in which the words exist.
    idf_dict = dict()

    for word in corpus:

        count = 0
        for document_number, words_in_it in corpus_dict.items():

            if word in words_in_it:

                count += 1

        if count == 0:

            continue

        else:
            
            idf_dict[word] = math.log(total_queries / count)

    return idf_dict


def generate_TFIDF(corpus, corpus_dict, tf_dict, idf_dict):
    """
    Function to generate TF-IDF for all the words.
    :param corpus: Corpus of words in the queries.
    :param corpus_dict: Mapping of query number and its corpus.
    :param tf_dict: Term Frequency Mapping.
    :param idf_dict: Inverse Document Frequency Mapping.
    :return tf_idf_dict: Term Frequency-Inverse Document Frequency Mapping.
    """

    tf_idf_dict = dict()

    for document_number, words_in_it in corpus_dict.items():

        tf_idf_dict_each = dict()
        for word in words_in_it:

            tf_idf_dict_each[word] = tf_dict[document_number][word] * idf_dict[word]

        tf_idf_dict[document_number] = tf_idf_dict_each

    return tf_idf_dict


def preprocess_queries():
    """
    Function to preprocess the user queries.
    return query_preprocessed: Preprocessed user queries.
    """

    # Some initializations..
    stopWords = set(nltk.corpus.stopwords.words("english"))
    ps = nltk.stem.PorterStemmer()

    # Get file path.
    queries_file_path = Path(QUERIES_PATH)

    # Lists to store the queries by line.
    contents, queries_by_lines, line = list(), list(), list()

    # Open file and store queries line by line.
    with open(queries_file_path) as f:

        c = f.read()
        contents = contents + nltk.word_tokenize(c)

    # Each query line ends with a period. So, using period as EOL.
    for query in contents:

        # If it ends with period, query ends here.
        if query != '.':

            line.append(query)

        else:

            queries_by_lines.append(line)
            line = list()

    # List to store the preprocessed queries.
    preprocessed_query = list()
    for contents in queries_by_lines:

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
        preprocessed_query.append(corpus)

    return preprocessed_query


def queries_cleaning():
    """
    Driver function to preprocess the queries and get inverted index.
    :return queries_TFIDF_dict: TF-IDF of the queries.
    """

    # Get the preprocessed queries.
    preprocessed_queries = preprocess_queries()

    # Get total number of queries for the IDF operation.
    total_queries = len(preprocessed_queries)

    # Flatten to get the vocabulary words.
    queries_corpus = list(set(list(sum(preprocessed_queries, []))))

    # Generate a dictionary of query number and words in it map.
    # Here, count denotes the query number.
    queries_corpus_dict = dict()
    count = 1
    for query in preprocessed_queries:

        queries_corpus_dict[count] = query
        count += 1

    # TF-IDF Operations.
    queries_TF_dict = generate_TF(queries_corpus, queries_corpus_dict)
    queries_IDF_dict = generate_IDF(queries_corpus, queries_corpus_dict, total_queries)
    queries_TFIDF_dict = generate_TFIDF(queries_corpus, queries_corpus_dict, queries_TF_dict, queries_IDF_dict)

    return queries_TFIDF_dict
