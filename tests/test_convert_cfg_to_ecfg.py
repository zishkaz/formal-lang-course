from pyformlang.cfg import CFG, Variable
from pyformlang.regular_expression import Regex

from project import convert_cfg_to_ecfg, regex_to_min_dfa


def check(cfg_as_text, expected_productions):
    ecfg = convert_cfg_to_ecfg(CFG.from_text(cfg_as_text))
    assert all(
        regex_to_min_dfa(ecfg.productions[production]).is_equivalent_to(
            regex_to_min_dfa(expected_productions[production])
        )
        for production in ecfg.productions
    )


def test_convert_cfg_to_ecfg_empty():
    cfg_as_text = ""
    expected_productions = {}
    check(cfg_as_text, expected_productions)


def test_convert_cfg_to_ecfg_1():
    cfg_as_text = "S -> x"
    expected_productions = {Variable("S"): Regex("x")}
    check(cfg_as_text, expected_productions)


def test_convert_cfg_to_ecfg_2():
    cfg_as_text = """
        S -> b|S*
    """
    expected_productions = {Variable("S"): Regex("b|S*")}
    check(cfg_as_text, expected_productions)
