from typing import Union

from pyformlang.regular_expression import Regex
from pyformlang.finite_automaton import DeterministicFiniteAutomaton


def regex_to_min_dfa(regex: Union[str, Regex]) -> DeterministicFiniteAutomaton:
    """Constructs minimal DFA based on the given regex.

    :param regex: String representation of a regex.
    :return: DFA corresponding to the given regex.
    """
    if isinstance(regex, str):
        regex = Regex(regex)
    epsilon_nfa = regex.to_epsilon_nfa()
    dfa = epsilon_nfa.to_deterministic()
    return dfa.minimize()
