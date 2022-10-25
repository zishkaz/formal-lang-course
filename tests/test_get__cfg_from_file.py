from pyformlang.cfg import Production, Terminal
from project.cfg import *
import os.path

test_dir_path = os.path.dirname(os.path.abspath(__file__))


def create_temp_file(file_name, text):
    cfg_file = os.sep.join([test_dir_path, file_name])
    with open(cfg_file, 'wt') as f:
        f.write(text)

    return cfg_file


def test_get_cfg_from_file():
    cfg_file = create_temp_file("not_empty_cfg.txt", "S -> x")
    cfg = get_cfg_from_file(cfg_file)
    expected = {Production(Variable("S"), [Terminal("x")])}
    assert cfg.productions == expected
    os.remove(cfg_file)


def test_get_cfg_from_file_not_default_start_symbol():
    cfg_file = create_temp_file("weird_start_symbol_cfg.txt", "A -> l")
    expected_start_symbol = Variable("A")
    cfg = get_cfg_from_file(cfg_file, expected_start_symbol)
    assert cfg.start_symbol == expected_start_symbol
    os.remove(cfg_file)


def test_get_cfg_from_file_empty():
    cfg_file = create_temp_file("empty_cfg.txt", "")
    cfg = get_cfg_from_file(cfg_file)
    assert cfg.is_empty()
    os.remove(cfg_file)
