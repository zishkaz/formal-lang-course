from pyformlang.cfg import Production, Terminal
from project.cfg import *


def test_cfg_to_weak_cnf_1():
    words_to_check = ["(())", "(", "((()))", "())"]
    cfg_text = """
        S -> ( S ) S
        S -> S ( S )
        S -> epsilon
    """
    weak_cnf = cfg_to_weak_cnf(CFG.from_text(cfg_text))
    expected = {
        Production(Variable("S"), []),
        Production(Variable(")#CNF#"), [Terminal(")")]),
        Production(Variable("(#CNF#"), [Terminal("(")]),
        Production(Variable("C#CNF#1"), [Variable("S"), Variable("C#CNF#2")]),
        Production(Variable("S"), [Variable("(#CNF#"), Variable("C#CNF#1")]),
        Production(Variable("C#CNF#2"), [Variable(")#CNF#"), Variable("S")]),
        Production(Variable("C#CNF#3"), [Variable("(#CNF#"), Variable("C#CNF#4")]),
        Production(Variable("S"), [Variable("S"), Variable("C#CNF#3")]),
        Production(Variable("C#CNF#4"), [Variable("S"), Variable(")#CNF#")]),
    }
    assert weak_cnf.productions == expected
    assert all(
        CFG.from_text(cfg_text).contains(word) == weak_cnf.contains(word)
        for word in words_to_check
    )


def test_cfg_to_weak_cnf_2():
    words_to_check = ["a", "aaaa", "ab", "caaaaa"]
    cfg_text = """
        S -> a S
        S -> epsilon
    """
    weak_cnf = cfg_to_weak_cnf(CFG.from_text(cfg_text))
    expected = {
        Production(Variable("S"), []),
        Production(Variable("a#CNF#"), [Terminal("a")]),
        Production(Variable("S"), [Variable("a#CNF#"), Variable("S")]),
    }
    assert weak_cnf.productions == expected
    assert all(
        CFG.from_text(cfg_text).contains(word) == weak_cnf.contains(word)
        for word in words_to_check
    )
