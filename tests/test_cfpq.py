from pyformlang.cfg import CFG

from project import cfpq, build_two_cycle_labeled_graph


def test_cfpq_1():
    cfg_as_text = """
            S -> epsilon
            """
    graph = build_two_cycle_labeled_graph(1, 1, ("A", "B"))
    reachable_pairs = {(0, 0), (1, 1), (2, 2)}
    assert cfpq(graph=graph, cfg=CFG.from_text(cfg_as_text)) == reachable_pairs


def test_cfpq_2():
    cfg_as_text = """
            S -> a S
            S -> epsilon
            """
    graph = build_two_cycle_labeled_graph(1, 1, ("a", "b"))
    reachable_pairs = {(0, 1), (0, 0), (1, 1), (2, 2), (1, 0)}
    assert cfpq(graph=graph, cfg=CFG.from_text(cfg_as_text)) == reachable_pairs


def test_cfpq_3():
    cfg_as_text = """
            S -> ( S ) S
            S -> S ( S )
            S -> epsilon
            """
    graph = build_two_cycle_labeled_graph(2, 3, ("a", "b"))
    reachable_pairs = {(4, 4), (5, 5), (0, 0), (1, 1), (3, 3), (2, 2)}
    assert (
        cfpq(
            graph=graph,
            cfg=CFG.from_text(cfg_as_text),
        )
        == reachable_pairs
    )
