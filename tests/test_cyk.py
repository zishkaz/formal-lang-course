from pyformlang.cfg import CFG

from project import cyk


def test_cyk_1():
    cfg = CFG.from_text(
        """
    S -> epsilon
    """
    )
    acceptable = [""]
    not_acceptable = ["a", "bbbc", " "]
    assert all(cyk(s, cfg) for s in acceptable) and all(
        not cyk(s, cfg) for s in not_acceptable
    )


def test_cyk_2():
    cfg = CFG.from_text(
        """
    S -> ( S ) S
    S -> S ( S )
    S -> epsilon
    """
    )
    acceptable = ["", "()", "()()", "((()))"]
    not_acceptable = ["((", "()(", "( S ) S", "bb", "aba", "bab"]
    assert all(cyk(s, cfg) for s in acceptable) and all(
        not cyk(s, cfg) for s in not_acceptable
    )


def test_cyk_3():
    cfg = CFG.from_text(
        """
    S -> a S
    S ->
    """
    )
    acceptable = ["a", "aaa", "", "aaaaaaaaaaaa"]
    not_acceptable = ["ba", "aaaab", "abbbaaa", "c"]
    assert all(cyk(s, cfg) for s in acceptable) and all(
        not cyk(s, cfg) for s in not_acceptable
    )
