from typing import NamedTuple, Set, Tuple, Union

import cfpq_data
import networkx.drawing.nx_pydot
from networkx import MultiDiGraph
from typing.io import IO
from pyformlang.finite_automaton import NondeterministicFiniteAutomaton


class GraphInfo(NamedTuple):
    """Class representing necessary data from a graph."""

    number_of_nodes: int
    number_of_edges: int
    edge_labels: Set[str]


def get_graph_info(graph: MultiDiGraph) -> GraphInfo:
    """Extracts number of nodes, edges and present edge labels from a graph.

    :param graph: Graph for info extraction.
    :return: Graph info.
    """
    edge_labels = set(label for _, _, label in graph.edges(data="label") if label)
    return GraphInfo(
        graph.number_of_nodes(),
        graph.number_of_edges(),
        edge_labels,
    )


def get_graph_info_by_name(graph_name: str) -> GraphInfo:
    """Loads graph by name from dataset and extracts info from it.

    :param graph_name: Graph name in the dataset.
    :return: Graph info.
    """
    graph = load_graph(graph_name)
    return get_graph_info(graph)


def build_two_cycle_labeled_graph(
    first_cycle_size: int,
    second_cycle_size: int,
    edge_labels: Tuple[str, str],
) -> MultiDiGraph:
    """Builds a labeled graph with two cycles.

    :param first_cycle_size: Number of nodes in the first cycle.
    :param second_cycle_size: Number of nodes in the second cycle.
    :param edge_labels: Edge labels.
    :return: Graph with two cycles connected by one node.
    """
    return cfpq_data.labeled_two_cycles_graph(
        n=first_cycle_size,
        m=second_cycle_size,
        labels=edge_labels,
    )


def build_and_save_two_cycle_labeled_graph(
    first_cycle_size: int,
    second_cycle_size: int,
    edge_labels: Tuple[str, str],
    file: Union[str, IO],
):
    """Builds and saves a labeled graph with two cycles.

    :param first_cycle_size: Number of nodes in the first cycle.
    :param second_cycle_size: Number of nodes in the second cycle.
    :param edge_labels: Edge labels.
    :param file: File handle to save with.
    """

    graph = build_two_cycle_labeled_graph(
        first_cycle_size=first_cycle_size,
        second_cycle_size=second_cycle_size,
        edge_labels=edge_labels,
    )
    save_graph(graph, file)


def load_graph(graph_name: str) -> MultiDiGraph:
    """Loads a graph from dataset.

    :param graph_name: Name of the graph.
    :return: Loaded graph.
    """
    graph_path = cfpq_data.download(graph_name)
    return cfpq_data.graph_from_csv(graph_path)


def save_graph(graph: MultiDiGraph, file: Union[str, IO]):
    """Saves a graph to a specified .dot file.

    :param graph: Graph to save.
    :param file: File handle to save with.
    """
    networkx.drawing.nx_pydot.write_dot(graph, file)


def build_nfa_by_graph(
    graph: MultiDiGraph, start_nodes: Set = None, final_nodes: Set = None
) -> NondeterministicFiniteAutomaton:
    """Builds NFA based on the given graph.

    :param graph: Graph to build corresponding NFA with.
    :param start_nodes: (optional) set of nodes to be used as start states in the built NFA.
    :param final_nodes: (optional) set of nodes to be used as final states in the built NFA.
    :return: NFA corresponding to the given graph.
    """
    nfa = NondeterministicFiniteAutomaton()
    all_nodes = set(graph.nodes)
    for node_from, node_to, label in graph.edges(data="label"):
        nfa.add_transition(node_from, label, node_to)

    if start_nodes is None:
        start_nodes = all_nodes
    for node in start_nodes:
        nfa.add_start_state(node)

    if final_nodes is None:
        final_nodes = all_nodes
    for node in final_nodes:
        nfa.add_final_state(node)

    return nfa
