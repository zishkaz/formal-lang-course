import networkx as nx

from project import build_two_cycle_labeled_graph, rpq_bfs


def make_graph():
    return build_two_cycle_labeled_graph(5, 3, ("A", "B"))


def test_rpq_bfs_empty_graph():
    graph = nx.MultiDiGraph()
    actual_rpq = rpq_bfs(
        graph=graph,
        query="A",
        all_reachable=True
    )
    assert not actual_rpq


def test_rpq_bfs_single_start_single_final():
    graph = make_graph()
    expected_rpq = {0: {6}}
    actual_rpq = rpq_bfs(
        graph=graph,
        query="AAAAAA|B",
        start_nodes={0},
        final_nodes={1, 2, 3, 4, 5, 6},
        all_reachable=True
    )
    assert actual_rpq == expected_rpq


def test_rpq_bfs_all_start_and_final():
    graph = make_graph()
    expected_rpq = {0, 6, 7, 8}
    actual_rpq = rpq_bfs(
        graph=graph,
        query="AAAAAA|B",
    )
    assert actual_rpq == expected_rpq
