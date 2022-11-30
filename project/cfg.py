from collections import defaultdict

import pyformlang
from pyformlang.cfg import CFG, Variable
from pyformlang.regular_expression import Regex

from project.ecfg import ECFG


def cfg_to_weak_cnf(cfg: CFG) -> CFG:
    """Converts Context Free Grammar to Weak Chomsky Normal Form.

    :param cfg: context free grammar to convert.
    :return: weak chomsky normal form of the given CFG.
    """
    cleared_cfg = (
        cfg.remove_useless_symbols()
        .eliminate_unit_productions()
        .remove_useless_symbols()
    )
    cleared_cfg_productions = cleared_cfg._decompose_productions(
        cleared_cfg._get_productions_with_only_single_terminals()
    )
    return CFG(
        start_symbol=cleared_cfg.start_symbol, productions=set(cleared_cfg_productions)
    )


def get_cfg_from_file(file: str, start_symbol: Variable = Variable("S")) -> CFG:
    """Loads Context Free Grammar from file.

    :param file: Containing file path.
    :param start_symbol: Grammar start symbol, defaults to "S".
    :return: Context Free Grammar.
    """
    with open(file) as f:
        return CFG.from_text(f.read(), start_symbol=start_symbol)


def convert_cfg_to_ecfg(cfg: CFG) -> ECFG:
    """Converts Context Free Grammar to Extended Context Free Grammar.

    :param cfg: Context Free Grammar.
    :return: Extended Context Free Grammar.
    """
    new_productions = defaultdict()
    for production in cfg.productions:
        regex = Regex(
            " ".join(
                "$" if isinstance(obj, pyformlang.cfg.Epsilon) else obj.value
                for obj in production.body
            )
            if len(production.body) > 0
            else "$"
        )
        new_productions[production.head] = (
            new_productions[production.head].union(regex)
            if production.head in new_productions
            else regex
        )
    return ECFG(
        start_symbol=cfg.start_symbol,
        variables=cfg.variables,
        productions=new_productions,
    )
