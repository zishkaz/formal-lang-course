from networkx import MultiDiGraph
from pyformlang.finite_automaton import NondeterministicFiniteAutomaton, State

from project import build_nfa_by_graph, build_two_cycle_labeled_graph


def test_check_is_nfa():
    two_cycles_graph = build_two_cycle_labeled_graph(
        first_cycle_size=4, second_cycle_size=4, edge_labels=("A", "B")
    )
    nfa = build_nfa_by_graph(two_cycles_graph)
    assert not nfa.is_deterministic()


def test_empty_graph_to_epsilon_nfa():
    empty_graph = MultiDiGraph()
    nfa = build_nfa_by_graph(empty_graph)
    assert nfa.is_empty()


def test_nfa_is_equivalent():
    expected_nfa = NondeterministicFiniteAutomaton()
    expected_nfa.add_transitions(
        [
            (0, "A", 1),
            (1, "A", 2),
            (2, "A", 3),
            (3, "A", 0),
            (0, "B", 4),
            (4, "B", 5),
            (5, "B", 6),
            (6, "B", 0),
        ]
    )

    start_states = {0, 1, 2, 3, 4, 5, 6}
    final_states = {0, 1, 2, 3, 4, 5, 6}

    for state in start_states:
        expected_nfa.add_start_state(State(state))
    for state in final_states:
        expected_nfa.add_final_state(State(state))

    two_cycles_graph = build_two_cycle_labeled_graph(
        first_cycle_size=3, second_cycle_size=3, edge_labels=("A", "B")
    )
    actual_nfa = build_nfa_by_graph(two_cycles_graph, start_states, final_states)
    assert actual_nfa.is_equivalent_to(expected_nfa)
