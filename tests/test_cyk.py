import os

from pyformlang.cfg import CFG

from project import cyk, get_word_from_file
from tests.test_get__cfg_from_file import create_temp_file


def test_cyk_1():
    cfg = CFG.from_text(
        """
    S -> epsilon
    """
    )
    file = create_temp_file("one_word.txt", "")
    acceptable = [get_word_from_file(file)]
    not_acceptable = ["a", "bbbc", " "]
    assert all(cyk(s, cfg) for s in acceptable) and all(
        not cyk(s, cfg) for s in not_acceptable
    )
    os.remove(file)


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
