from pyformlang.finite_automaton import NondeterministicFiniteAutomaton, State
from scipy import sparse


class AdjacencyMatrix:
    def __init__(self, nfa: NondeterministicFiniteAutomaton = None):
        if nfa is None:
            self.start_states = set()
            self.final_states = set()
            self.state_indices = dict()
            self.matrix = dict()
        else:
            self.start_states = nfa.start_states
            self.final_states = nfa.final_states
            self.state_indices = {
                state: index for index, state in enumerate(nfa.states)
            }
            self.matrix = self.__init_matrix__(nfa)

    def get_states_count(self):
        """
        :return: Count of states in the NFA.
        """
        return len(self.state_indices.keys())

    def get_states(self):
        """
        :return: States in the NFA.
        """
        return self.state_indices.keys()

    def get_start_states(self):
        """
        :return: Start states in the NFA.
        """
        return self.start_states

    def get_final_states(self):
        """
        :return: Final states in the NFA.
        """
        return self.final_states

    def __init_matrix__(self, n_automaton: NondeterministicFiniteAutomaton):
        result_matrix = dict()
        nfa_dict = n_automaton.to_dict()
        for state_from, transition in nfa_dict.items():
            for label, states_to in transition.items():
                if not isinstance(states_to, set):
                    states_to = {states_to}
                for state_to in states_to:
                    index_from = self.state_indices[state_from]
                    index_to = self.state_indices[state_to]
                    if label not in result_matrix:
                        result_matrix[label] = sparse.csr_matrix(
                            (self.get_states_count(), self.get_states_count()),
                            dtype=bool,
                        )
                    result_matrix[label][index_from, index_to] = True

        return result_matrix

    def make_transitive_closure(self):
        """
        :return: Transitive closure of the adjacency matrix.
        """
        result = sum(self.matrix.values())
        curr_nnz = 0
        prev_nnz = result.nnz

        while prev_nnz != curr_nnz:
            result += result.__matmul__(result)
            prev_nnz = curr_nnz
            curr_nnz = result.nnz

        return result


def intersect_adjacency_matrices(
    first_matrix: AdjacencyMatrix, second_matrix: AdjacencyMatrix
):
    """
    Calculates tensor multiplication of two adjacency matrices.
    :return: Result matrix.
    """
    result = AdjacencyMatrix()
    common_symbols = first_matrix.matrix.keys().__and__(second_matrix.matrix.keys())

    for symbol in common_symbols:
        result.matrix[symbol] = sparse.kron(
            first_matrix.matrix[symbol], second_matrix.matrix[symbol], format="csr"
        )

    for state_first, state_first_index in first_matrix.state_indices.items():
        for state_second, state_second_index in second_matrix.state_indices.items():
            new_state_index = (
                state_first_index * second_matrix.get_states_count()
                + state_second_index
            )
            new_state = new_state_index
            result.state_indices[new_state] = new_state_index

            if (
                state_first in first_matrix.start_states
                and state_second in second_matrix.start_states
            ):
                result.start_states.add(new_state)

            if (
                state_first in first_matrix.final_states
                and state_second in second_matrix.final_states
            ):
                result.final_states.add(new_state)

    return result


def am_to_nfa(am: AdjacencyMatrix):
    """
    :param am: Adjacency matrix.
    :return: NFA representing the given matrix.
    """
    automaton = NondeterministicFiniteAutomaton()
    for label, bool_matrix in am.matrix.items():
        for state_from, state_to in zip(*bool_matrix.nonzero()):
            automaton.add_transition(state_from, label, state_to)

    for state in am.start_states:
        automaton.add_start_state(State(state))

    for state in am.final_states:
        automaton.add_final_state(State(state))

    return automaton
