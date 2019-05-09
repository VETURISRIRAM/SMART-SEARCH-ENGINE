"""
@author: Sriram Veturi
@title: SmartSearch - An Intelligent Search Engine.
@date: 05/06/2019
"""

import os
import json

from queries_cleaning_processing import queries_cleaning

TF_IDF_FILES_DIR = "./tf_idf_files"
DATA_DIR = "./documents"

def cosineSimilarityCalculator(documents_TFIDF_dict, queries_TFIDF_dict):
    """
    Function to calculate the cosine similarity between documents and the queries.
    :param documents_TFIDF_dict: TF-IDF Map of all the urls.
    :param queries_TFIDF_dict: TF-IDF Map of all the queries.
    :return queries_documents_similarity: Cosine Similarity (CS) score between documents and urls.
    """

    # To store the CS score.
    queries_documents_similarity = dict()

    for query, query_words_and_weight_dict in queries_TFIDF_dict.items():

        query_documents_similarity = dict()
        for document, document_words_and_weights_dict in documents_TFIDF_dict.items():

            # Find intersection. If there is atleast one word in common, get CS score.
            intersection = [i for i in list(query_words_and_weight_dict.keys()) if
                            i in list(document_words_and_weights_dict.keys())]

            # If there is no word in common between doc and query, do not calculate CS score for the doc.
            if len(intersection) == 0:

                continue

            # Else perform and calculate CS score.
            else:

                try:

                    # Formula: Similarity(A,B) = (A.B)/((||A||)*(||B||)).
                    # Therefore, numerator is (A.B) and denominator is ((||A||)*(||B||)).

                    # Calculate the numerator.
                    numerator = 0
                    for commonWord in intersection:

                        numerator += query_words_and_weight_dict[commonWord] * document_words_and_weights_dict[commonWord]

                    # Calculate the denominator
                    doc_term = 0
                    for doc_words, word_weights in document_words_and_weights_dict.items():

                        doc_term += (word_weights) ** 2

                    doc_term = (doc_term) ** (1 / 2)
                    query_term = 0
                    for queryWord, word_weights in query_words_and_weight_dict.items():

                        query_term += (word_weights) ** 2

                    query_term = (query_term) ** (1 / 2)
                    denominator = doc_term * query_term
                    cosine_similarity = numerator / denominator

                except:

                    continue

            index = '(' + str(query) + ',' + str(document) + ')'
            query_documents_similarity[index] = cosine_similarity

        # Sort the similarities in descending order
        query_documents_similarity = sorted(query_documents_similarity.items(), key=lambda kv: kv[1])[::-1]
        temp = dict()
        for x in query_documents_similarity:

            temp[x[0]] = x[1]

        if len(temp) != 0:

            queries_documents_similarity[query] = temp

    return queries_documents_similarity


def get_top_200_similar_urls():
    """
    Function to get the top 200 relevant urls for the queries.
    """

    # Get all the urls sorted in the relevance order.
    retrieved_urls_in_relevance_order = get_cosine_similarity()

    # Dictionary to store query numbers and their top 200 matching urls
    top_urls_math_map = dict()

    # Sorry for the huge variable names. But it makes sense.
    for query_number, retrieved_urls_similarity_score_map in retrieved_urls_in_relevance_order.items():

        top_urls = list()

        # Get top 200 urls.
        all_urls = list(retrieved_urls_similarity_score_map.keys())[:200]

        for url in all_urls:

            # URLS here are in the string form as '(1,https://cs.uic.edu/faculty-staff/)'
            # So, to get only the url, get the substring between comma and the closing bracket.
            # Hence, some crappy string formatting.
            comma_index = url.index(",")
            closing_bracket_index = url.index(")")

            top_urls.append(url[comma_index + 1 : closing_bracket_index])

        top_urls_math_map[query_number] = top_urls
        
    return top_urls_math_map


def get_cosine_similarity():
    """
    Driver function to get the cosine similarity between documents and queries.
    return cosine_similarity: Cosine Similarity between documents and queries.
    """

    # Get the TF-IDF of the queries.
    queries_tf_idf = queries_cleaning()

    # Open the documents saved TF-IDF map.
    with open(os.path.join(TF_IDF_FILES_DIR, "tf_idf.json"), "r") as doc_tf_idf_file:

        documents_tf_idf = dict(json.load(doc_tf_idf_file))

    # Get the cosine similarity between documents and queries.
    similarity = cosineSimilarityCalculator(documents_tf_idf, queries_tf_idf)

    return similarity
