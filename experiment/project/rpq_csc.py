from typing import Iterable, Union, Set, Dict

import networkx as nx

from project import build_nfa_by_graph, regex_to_min_dfa

from project.adjacency_matrix_csc import (
    AdjacencyMatrixCsc,
    intersect_adjacency_matrices,
    sync_bfs,
)


def rpq_tensor_csc(
    graph: nx.MultiDiGraph,
    query: str,
    start_nodes: set = None,
    final_nodes: set = None,
):
    """Calculates Regular Path Querying using tensor multiplication from given graph and regular expression.
    :param graph: Graph to send query to.
    :param query: A graph query.
    :param start_nodes: Set of start nodes of the graph.
    :param final_nodes: Set of final nodes of the graph.
    :return: Regular Path Querying as set.
    """
    nfa = build_nfa_by_graph(graph, start_nodes, final_nodes)
    dfa = regex_to_min_dfa(query)

    graph_matrix = AdjacencyMatrixCsc(nfa)
    query_matrix = AdjacencyMatrixCsc(dfa)

    intersected_matrix = intersect_adjacency_matrices(graph_matrix, query_matrix)
    transitive_closure = intersected_matrix.make_transitive_closure()

    start_states = intersected_matrix.get_start_states()
    final_states = intersected_matrix.get_final_states()

    result = set()

    for state_from, state_to in zip(*transitive_closure.nonzero()):
        if state_from in start_states and state_to in final_states:
            result.add(
                (
                    state_from // query_matrix.get_states_count(),
                    state_to // query_matrix.get_states_count(),
                )
            )

    return result


def rpq_bfs_csc(
    query: str,
    graph: nx.MultiDiGraph,
    start_nodes: Iterable[int] = None,
    final_nodes: Iterable[int] = None,
    all_reachable: bool = False,
) -> Union[Set[int], Dict[int, Set[int]]]:
    """Calculates Regular Path Querying using multiple source BFS from given graph and regular expression.
    :param graph: Graph to send query to.
    :param query: A graph query.
    :param start_nodes: Set of start nodes of the graph.
    :param final_nodes: Set of final nodes of the graph.
    :param all_reachable: [Used in sync_bfs function] Specifies whether for each start node will be returned a set of reachable
                          nodes as Dict, or all reachable nodes as Set from the given start nodes set (True for Set, False for Dict).
    :return: Regular Path Querying in format depending on all_reachable flag.
    """
    am1 = AdjacencyMatrixCsc(build_nfa_by_graph(graph, start_nodes, final_nodes))
    am2 = AdjacencyMatrixCsc(regex_to_min_dfa(query))
    result = sync_bfs(am1, am2, all_reachable)
    return (
        {start.value: {end.value for end in ends} for (start, ends) in result.items()}
        if all_reachable
        else {end.value for end in result}
    )
