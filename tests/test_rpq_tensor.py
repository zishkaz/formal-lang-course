from project import build_two_cycle_labeled_graph, rpq_tensor
import networkx as nx


def make_graph_two_cycled():
    return build_two_cycle_labeled_graph(5, 3, ("A", "B"))


def make_graph():
    graph = nx.MultiDiGraph()
    graph.add_edge(0, 1, label="A")
    graph.add_edge(0, 2, label="B")
    graph.add_edge(1, 3, label="C")
    graph.add_edge(1, 3, label="D")
    graph.add_edge(2, 3, label="C")
    graph.add_edge(2, 3, label="D")
    graph.add_edge(3, 4, label="E")
    graph.add_edge(4, 5, label="E")
    return graph


def test_rpq_tensor_1():
    query = "AAAAAA|B"
    start_nodes = {0}
    final_nodes = {1, 2, 3, 4, 5, 6}
    graph = make_graph_two_cycled()
    actual_rpq = rpq_tensor(graph, query, start_nodes, final_nodes)
    expected_rpq = {(0, 6)}
    assert actual_rpq == expected_rpq


def test_rpq_tensor_2():
    query = "(A|B)C(D*)(E*)"
    start_nodes = {0}
    final_nodes = {3}
    graph = make_graph()
    actual_rpq = rpq_tensor(graph, query, start_nodes, final_nodes)
    expected_rpq = {(0, 3)}
    assert actual_rpq == expected_rpq


def test_rpq_tensor_3():
    query = "(A*)(C*)(E*)"
    start_nodes = {0}
    final_nodes = {4, 5}
    graph = make_graph()
    actual_rpq = rpq_tensor(graph, query, start_nodes, final_nodes)
    expected_rpq = {(0, 4), (0, 5)}
    assert actual_rpq == expected_rpq
