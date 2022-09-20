from pyformlang.regular_expression import Regex
from pyformlang.finite_automaton import DeterministicFiniteAutomaton


def regex_to_min_dfa(regex_str: str) -> DeterministicFiniteAutomaton:
    """Constructs minimal DFA based on the given regex.

    :param regex_str: String representation of a regex.
    :return: DFA corresponding to the given regex.
    """

    regex = Regex(regex_str)
    epsilon_nfa = regex.to_epsilon_nfa()
    dfa = epsilon_nfa.to_deterministic()
    return dfa.minimize()
