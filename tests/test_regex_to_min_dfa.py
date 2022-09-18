from project.regex import regex_to_min_dfa
from pyformlang.finite_automaton import Symbol, State, DeterministicFiniteAutomaton

test_regex = "a b c* d"


def test_creating_min_dfa_from_regex():
    actual_dfa = regex_to_min_dfa(test_regex)
    expected = DeterministicFiniteAutomaton()

    state_0 = State(0)
    state_1 = State(1)
    state_2 = State(2)
    state_3 = State(3)

    symbol_a = Symbol("a")
    symbol_b = Symbol("b")
    symbol_c = Symbol("c")
    symbol_d = Symbol("d")

    expected.add_start_state(state_0)
    expected.add_final_state(state_3)

    expected.add_transition(state_0, symbol_a, state_1)
    expected.add_transition(state_1, symbol_b, state_2)
    expected.add_transition(state_2, symbol_c, state_2)
    expected.add_transition(state_2, symbol_d, state_3)
    assert (
        expected.is_equivalent_to(actual_dfa)
        and actual_dfa.is_deterministic()
        and expected.minimize().is_equivalent_to(expected)
    )


def test_min_dfa_accepts_same_language():
    dfa = regex_to_min_dfa(test_regex)
    accepted = [
        [Symbol("a"), Symbol("b"), Symbol("d")],
        [Symbol("a"), Symbol("b"), Symbol("c"), Symbol("d")],
        [Symbol("a"), Symbol("b"), Symbol("c"), Symbol("c"), Symbol("d")],
        [Symbol("a"), Symbol("b"), Symbol("c"), Symbol("c"), Symbol("c"), Symbol("d")],
    ]
    not_accepted = [
        [Symbol("b"), Symbol("c"), Symbol("d")],
        [Symbol("")],
        [Symbol("a"), Symbol("b"), Symbol("c")],
    ]
    assert all(dfa.accepts(word) for word in accepted) and all(
        not dfa.accepts(word) for word in not_accepted
    )
