from project import build_two_cycle_labeled_graph, rpq


def make_graph():
    return build_two_cycle_labeled_graph(5, 3, ("A", "B"))


def test_rpq():
    query = "AAAAAA|B"
    start_nodes = {0}
    final_nodes = {1, 2, 3, 4, 5, 6}
    graph = make_graph()
    actual_rpq = rpq(graph, query, start_nodes, final_nodes)
    expected_rpq = {(0, 6)}
    assert actual_rpq == expected_rpq
