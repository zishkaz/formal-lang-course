from typing import NamedTuple, AbstractSet

from pyformlang.cfg import Variable
from pyformlang.regular_expression import Regex

from project.rsm import RSM


class ECFG(NamedTuple):

    start_symbol: Variable
    variables: AbstractSet[Variable]
    productions: dict[Variable, Regex]


def get_ecfg_from_text(text: str, start_symbol: Variable = Variable("S")):
    """Constructs Extended Context Free Grammar from text representation.

    :param text: Text representation of extended Context Free Grammar.
    :param start_symbol: Start symbol of given extended Context Free Grammar.
    :return: Extended Context Free Grammar.
    """
    variables = set()
    productions = dict()
    for line in text.splitlines():
        if not line.strip():
            continue
        content = [str.strip(elem) for elem in line.split("->")]
        head, body = content
        head = Variable(head)
        body = Regex(body)
        variables.add(head)
        productions[head] = body
    return ECFG(
        start_symbol=start_symbol,
        variables=variables,
        productions=productions,
    )


def get_ecfg_from_file(
        file: str, start_symbol: Variable = Variable("S")
) -> ECFG:
    """Constructs Extended Context Free Grammar from file.

    :param file: Path to file.
    :param start_symbol: Start symbol of given extended Context Free Grammar.
    :return: Extended Context Free Grammar.
    """
    with open(file) as f:
        return get_ecfg_from_text(f.read(), start_symbol=start_symbol)


def convert_ecfg_to_rsm(ecfg: ECFG) -> RSM:
    """Converts Extended Context Free Grammar to Recursive State Machine.

    :param ecfg: Given extended Context Free Grammar.
    :return: Recursive State Machine from extended Context Free Grammar.
    """
    return RSM(
        start_symbol=ecfg.start_symbol,
        boxes={h: r.to_epsilon_nfa().to_deterministic() for h, r in ecfg.productions.items()},
    )