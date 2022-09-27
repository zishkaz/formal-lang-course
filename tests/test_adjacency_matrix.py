from pyformlang.finite_automaton import (
    NondeterministicFiniteAutomaton,
    State,
    DeterministicFiniteAutomaton,
)

from project import AdjacencyMatrix, intersect_adjacency_matrices, am_to_nfa


def make_nfa():
    nfa = NondeterministicFiniteAutomaton()
    nfa.add_transitions(
        [
            (0, "A", 1),
            (1, "B", 2),
            (1, "C", 1),
            (2, "Z", 3),
            (3, "V", 0),
        ]
    )

    return nfa


def test_nnz():
    nfa = make_nfa()
    label = "A"
    expected_nnz = 1
    am = AdjacencyMatrix(nfa)
    actual_nnz = am.matrix[label].nnz
    assert actual_nnz == expected_nnz


def test_adjacency():
    nfa = make_nfa()
    label = "A"
    edges = [(0, 1)]
    bm = AdjacencyMatrix(nfa)
    assert all(bm.matrix[label][edge] for edge in edges)


def test_tc():
    nfa = make_nfa()
    am = AdjacencyMatrix(nfa)
    tc = am.make_transitive_closure()
    assert tc.sum() == tc.size


def test_intersection():
    fa1 = NondeterministicFiniteAutomaton()
    fa1.add_transitions(
        [(0, "A", 1), (0, "B", 0), (1, "C", 1), (1, "Z", 2), (2, "V", 0)]
    )
    fa1.add_start_state(State(0))
    fa1.add_final_state(State(0))
    fa1.add_final_state(State(1))
    fa1.add_final_state(State(2))

    am1 = AdjacencyMatrix(fa1)
    fa2 = NondeterministicFiniteAutomaton()
    fa2.add_transitions([(0, "A", 1), (1, "P", 2)])
    fa2.add_start_state(State(0))
    fa2.add_final_state(State(1))

    am2 = AdjacencyMatrix(fa2)
    expected_fa = DeterministicFiniteAutomaton()
    expected_fa.add_transitions([(0, "A", 1)])
    expected_fa.add_start_state(State(0))
    expected_fa.add_final_state(State(1))

    intersected_bm = intersect_adjacency_matrices(am1, am2)
    actual_fa = am_to_nfa(intersected_bm)
    assert actual_fa.is_equivalent_to(expected_fa)
