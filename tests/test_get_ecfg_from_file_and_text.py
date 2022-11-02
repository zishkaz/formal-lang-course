import os

from pyformlang.cfg import Variable

from project import get_ecfg_from_file, get_ecfg_from_text
from tests.test_get__cfg_from_file import create_temp_file


def test_get_ecfg_from_file_not_empty():
    ecfg_file = create_temp_file("not_empty_ecfg.txt", "S -> x")
    ecfg = get_ecfg_from_file(ecfg_file)
    expected_productions = {Variable("S"): "x"}
    productions = {left: str(rule) for left, rule in ecfg.productions.items()}
    assert productions == expected_productions
    os.remove(ecfg_file)


def test_get_ecfg_from_file_empty():
    ecfg_file = create_temp_file("empty_ecfg.txt", "")
    ecfg = get_ecfg_from_file(ecfg_file)
    expected_productions = {}
    assert ecfg.productions == expected_productions
    os.remove(ecfg_file)

def test_get_ecfg_from_text_not_empty():
    ecfg = get_ecfg_from_text("S -> x")
    expected_productions = {Variable("S"): "x"}
    productions = {left: str(rule) for left, rule in ecfg.productions.items()}
    assert productions == expected_productions


def test_get_ecfg_from_text_empty():
    ecfg = get_ecfg_from_text("")
    expected_productions = {}
    assert ecfg.productions == expected_productions
