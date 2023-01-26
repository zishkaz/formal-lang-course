from collections import defaultdict
from typing import Dict, Set, Union

from pyformlang.finite_automaton import NondeterministicFiniteAutomaton, State
from scipy import sparse
from scipy.sparse import dok_matrix


class AdjacencyMatrixCsc:
    def __init__(
        self,
        nfa: NondeterministicFiniteAutomaton = None,
        state_to_index: Dict = None,
        start_states: Set = None,
        final_states: Set = None,
        matrix: Dict = None,
    ):
        if nfa is not None:
            self.start_states = nfa.start_states.copy()
            self.final_states = nfa.final_states.copy()
            self.state_indices = {
                state: index for index, state in enumerate(nfa.states)
            }
            self.matrix = self.__init_matrix__(nfa)
        elif (
            (state_to_index is not None)
            and (start_states is not None)
            and (final_states is not None)
            and (matrix is not None)
        ):
            self.start_states = start_states
            self.final_states = final_states
            self.state_indices = state_to_index
            self.matrix = matrix
        else:
            self.start_states = set()
            self.final_states = set()
            self.state_indices = dict()
            self.matrix = dict()

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

    def index_by_state(self, state):
        return self.state_indices[state]

    def state_by_index(self, index):
        for state, ind in self.state_indices.items():
            if ind == index:
                return state

    def get_final_states(self):
        """
        :return: Final states in the NFA.
        """
        return self.final_states

    def __init_matrix__(self, n_automaton: NondeterministicFiniteAutomaton):

        result_matrix = defaultdict(
            lambda: dok_matrix(
                (len(n_automaton.states), len(n_automaton.states)), dtype=bool
            )
        )
        state_from_to_transition = n_automaton.to_dict()
        for label in n_automaton.symbols:
            for state_from, transitions in state_from_to_transition.items():
                states_to = transitions.get(label, set())
                if not isinstance(states_to, set):
                    states_to = {states_to}
                for state_to in states_to:
                    index_from = self.state_indices[state_from]
                    index_to = self.state_indices[state_to]
                    result_matrix[label][index_from, index_to] = True
        return result_matrix

    def make_transitive_closure(self):
        """
        :return: Transitive closure of the adjacency matrix.
        """
        result = sum(
            self.matrix.values(),
            start=dok_matrix((len(self.state_indices), len(self.state_indices))),
        )
        curr_nnz = 0
        prev_nnz = result.nnz

        while prev_nnz != curr_nnz:
            result += result.__matmul__(result)
            prev_nnz = curr_nnz
            curr_nnz = result.nnz

        return result


def intersect_adjacency_matrices(
    first_matrix: AdjacencyMatrixCsc, second_matrix: AdjacencyMatrixCsc
):
    """
    Calculates tensor multiplication of two adjacency matrices.
    :return: Result matrix.
    """
    result = AdjacencyMatrixCsc()
    common_symbols = first_matrix.matrix.keys().__and__(second_matrix.matrix.keys())

    for symbol in common_symbols:
        result.matrix[symbol] = sparse.kron(
            first_matrix.matrix[symbol], second_matrix.matrix[symbol], format="csc"
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


def am_to_nfa(am: AdjacencyMatrixCsc):
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


def make_front(
    start_state_indices,
    first_matrix: AdjacencyMatrixCsc,
    second_matrix: AdjacencyMatrixCsc,
) -> sparse.csc_matrix:
    front_row = sparse.dok_matrix((1, first_matrix.get_states_count()), dtype=bool)
    for i in start_state_indices:
        front_row[0, i] = True
    front_row = front_row.tocsc()
    front = sparse.csc_matrix(
        (second_matrix.get_states_count(), first_matrix.get_states_count()), dtype=bool
    )
    for i in map(
        lambda state: second_matrix.index_by_state(state), second_matrix.start_states
    ):
        front[i, :] = front_row
    return front


def get_reachable(
    sub_front_idx,
    first_matrix: AdjacencyMatrixCsc,
    second_matrix: AdjacencyMatrixCsc,
    visited,
) -> Set[State]:
    sub_front_offset = sub_front_idx * second_matrix.get_states_count()
    reachable = sparse.csc_matrix((1, first_matrix.get_states_count()), dtype=bool)
    for i in map(
        lambda state: second_matrix.index_by_state(state), second_matrix.final_states
    ):
        reachable += visited[sub_front_offset + i, :]
    return set(
        first_matrix.state_by_index(i)
        for i in reachable.nonzero()[1]
        if i
        in map(
            lambda state: first_matrix.index_by_state(state), first_matrix.final_states
        )
    )


def sync_bfs(
    first_matrix: AdjacencyMatrixCsc,
    second_matrix: AdjacencyMatrixCsc,
    all_reachable: bool = False,
) -> Union[Set[State], Dict[State, Set[State]],]:
    """Performs synchronized BFS on two NFA's.
    :param all_reachable: Specifies whether for each start node will be returned a set of reachable nodes as Dict,
                          or all reachable nodes as Set from the given start nodes set (True for Set, False for Dict)
    :return: Reachable nodes depending on all_reachable flag.
    """
    if not first_matrix.start_states:
        return dict() if all_reachable else set()

    common_symbols = first_matrix.matrix.keys().__and__(second_matrix.matrix.keys())
    front = (
        sparse.vstack(
            [
                make_front({i}, first_matrix, second_matrix)
                for i in map(
                    lambda state: first_matrix.index_by_state(state),
                    first_matrix.start_states,
                )
            ]
        )
        if all_reachable
        else make_front(
            map(
                lambda state: first_matrix.index_by_state(state),
                first_matrix.start_states,
            ),
            first_matrix,
            second_matrix,
        )
    )
    visited = front
    while True:
        next_front = sparse.csc_matrix(front.shape, dtype=bool)
        for label in common_symbols:
            next_front_part = front.__matmul__(first_matrix.matrix[label])
            for index in range(len(first_matrix.start_states) if all_reachable else 1):
                offset = index * second_matrix.get_states_count()
                for (i, j) in zip(*second_matrix.matrix[label].nonzero()):
                    next_front[offset + j, :] += next_front_part[offset + i, :]
        front = next_front > visited
        visited += front
        if front.count_nonzero() == 0:
            break

    return (
        {
            first_matrix.state_by_index(start_state_idx): get_reachable(
                sub_front_idx, first_matrix, second_matrix, visited
            )
            for sub_front_idx, start_state_idx in enumerate(
                map(
                    lambda state: first_matrix.index_by_state(state),
                    first_matrix.start_states,
                )
            )
        }
        if all_reachable
        else get_reachable(0, first_matrix, second_matrix, visited)
    )
