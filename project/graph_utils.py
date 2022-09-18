from typing import NamedTuple, Set, Tuple, Union

from cfpq_data import *
import networkx.drawing.nx_pydot
from networkx import MultiDiGraph
from typing.io import IO


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
    return labeled_two_cycles_graph(
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
    graph_path = download(graph_name)
    return graph_from_csv(graph_path)


def save_graph(graph: MultiDiGraph, file: Union[str, IO]):
    """Saves a graph to a specified .dot file.

    :param graph: Graph to save.
    :param file: File handle to save with.
    """
    networkx.drawing.nx_pydot.write_dot(graph, file)
