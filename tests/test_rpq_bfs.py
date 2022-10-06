import networkx as nx

from project import build_two_cycle_labeled_graph, rpq_bfs


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


def test_rpq_bfs_empty_graph():
    graph = nx.MultiDiGraph()
    actual_rpq = rpq_bfs(graph=graph, query="A", all_reachable=True)
    assert not actual_rpq


def test_rpq_bfs_single_start_single_final():
    graph = make_graph_two_cycled()
    expected_rpq = {0: {6}}
    actual_rpq = rpq_bfs(
        graph=graph,
        query="AAAAAA|B",
        start_nodes={0},
        final_nodes={1, 2, 3, 4, 5, 6},
        all_reachable=True,
    )
    assert actual_rpq == expected_rpq


def test_rpq_bfs_all_start_and_final():
    graph = make_graph_two_cycled()
    expected_rpq = {0, 6, 7, 8}
    actual_rpq = rpq_bfs(
        graph=graph,
        query="AAAAAA|B",
    )
    assert actual_rpq == expected_rpq


def test_rpq_bfs_1():
    graph = make_graph()
    expected_rpq = {3}
    actual_rpq = rpq_bfs(
        graph=graph,
        query="(A|B)C(D*)(E*)",
        start_nodes={0},
        final_nodes={3}
    )
    assert actual_rpq == expected_rpq


def test_rpq_bfs_2():
    graph = make_graph()
    expected_rpq = {0: {4, 5}}
    actual_rpq = rpq_bfs(
        graph=graph,
        query="(A*)(C*)(E*)",
        start_nodes={0},
        final_nodes={4, 5},
        all_reachable=True
    )
    assert actual_rpq == expected_rpq


