import networkx as nx

from project import build_nfa_by_graph, regex_to_min_dfa
from project.matrix import AdjacencyMatrix, intersect_adjacency_matrices


def rpq(
        graph: nx.MultiDiGraph,
        query: str,
        start_nodes: set = None,
        final_nodes: set = None,
):
    """Calculates Regular Path Querying from given graph and regular expression.
    :param graph: Graph to send query to.
    :param query: A graph query.
    :param start_nodes: Set of start nodes of the graph.
    :param final_nodes: Set of final nodes of the graph.
    :return: Regular Path Querying as set.
    """
    nfa = build_nfa_by_graph(graph, start_nodes, final_nodes)
    dfa = regex_to_min_dfa(query)

    graph_matrix = AdjacencyMatrix(nfa)
    query_matrix = AdjacencyMatrix(dfa)

    intersected_matrix = intersect_adjacency_matrices(graph_matrix, query_matrix)
    transitive_closure = intersected_matrix.make_transitive_closure()

    start_states = intersected_matrix.get_start_states()
    final_states = intersected_matrix.get_final_states()

    result = set()

    for state_from, state_to in zip(*transitive_closure.nonzero()):
        if state_from in start_states and state_to in final_states:
            result.add(
                (state_from // query_matrix.get_states_count(), state_to // query_matrix.get_states_count())
            )

    return result
