"""
@author: Sriram Veturi
@title: SmartSearch - An Intelligent Search Engine.
@date: 05/06/2019
"""

############################################################################################
# PAGE RANK FORMULA (S(A)) = EPSILON        (1 - EPSILON) * SUM OF ALL B's -> A :  S (B)   #
#                            -------   +                                         --------- #
#                               N                                                 OUT (B)  #
############################################################################################

import operator
import numpy as np

# Globals..
EPSILON = 0.15

# It takes 52 iterations to get converging page ranks of a web graph with 322 Million documents.
# Our data has close to 5000 documents. For this web graph, 20 iterations is more than enough.
ITERATIONS = 20


def get_incoming_connections(web_graph):
    """
    Function to get the number of incoming nodes because "S (B)" in the formula.
    :param web_graph: The dictionary structure of the web structure.
    :return incomming_connections: Incomming nodes dicitonary.
    """

    # Nodes in the web graph
    web_graph_nodes = list(web_graph.keys())

    # Get the incoming connections
    incoming_connections = dict()

    for parent_node, outgoing_connections in web_graph.items():

        for child_node in outgoing_connections:

            if child_node not in incoming_connections:

                incoming_connections[child_node] = [parent_node]

            else:

                incoming_connections[child_node].append(parent_node)

    # Some nodes do not have any incoming connections.
    # For them initialize an empty list.
    for node in web_graph_nodes:

        if node not in incoming_connections:

            incoming_connections[node] = []

    return incoming_connections


def get_outgoing_connections_count(web_graph):
    """
    Function to get the number of outgoing links of a node because of "OUT (B)" in the formula.
    :param web_graph: The dictionary structure of the web structure.
    :return outgoing_number_of_connections: The numbe of outgoing links.
    """

    # Build outgoing connections number
    outgoing_number_of_connections = dict()
    for parent_node, outgoing_connections in web_graph.items():

        outgoing_number_of_connections[parent_node] = len(outgoing_connections)

    return outgoing_number_of_connections


def get_page_ranks(web_graph):
    """
    Main function for the Page Rank Algorithm happens here.
    :paran web_graph: The dictionary structure of the web structure.
    :return sorted_final_page_ranks: Converged and sorted page ranks of all nodes in the web graph.
    """

    # Nodes in the web graph.
    web_graph_nodes = list(web_graph.keys())

    # Number of outgoing connections.
    outgoing_number_of_connections = get_outgoing_connections_count(web_graph)

    # Incoming connections nodes.
    incoming_connections = get_incoming_connections(web_graph)

    # Total number of nodes (N).
    total_nodes = len(web_graph_nodes)

    # Initialize page rank scores. 
    # All nodes have 1 / N.
    page_rank_scores = dict()
    for node in web_graph_nodes:

        page_rank_scores[node] = 1 / total_nodes

    # Initialize it to zeroth iteration.
    page_rank_dict = dict()
    page_rank_dict[0] = page_rank_scores

    # Iterate and update the page ranks for 20 iterations or convergence whichever comes first.
    for i in range(1, ITERATIONS):
        print("Page Rank Iteration:", i)

        node_rank_dict = dict()
        for node in web_graph_nodes:

            # Get all the incoming nodes for this node.
            incoming_nodes = incoming_connections[node]

            # Now, get this part of formula.
            # SUM OF ALL B -> A : S(B) / ALL_OUT(B)
            temp_score = 0
            for incoming_node in incoming_nodes:

                # Update based on previous iteration's page ranks.
                previous_page_ranks_dict = page_rank_dict[i - 1]
                temp_score += (previous_page_ranks_dict[incoming_node] / outgoing_number_of_connections[incoming_node])

            # Now, calculate new page rank.
            rank_score = (EPSILON / total_nodes) + ((1 - EPSILON) * temp_score)
            node_rank_dict[node] = rank_score

        page_rank_dict[i] = node_rank_dict

        # Breaking condition.
        if page_rank_dict[i] == page_rank_dict[i - 1]:

            break

    final_page_ranks = node_rank_dict
    sorted_final_page_ranks = sorted(final_page_ranks.items(), key=operator.itemgetter(1))

    return sorted_final_page_ranks
