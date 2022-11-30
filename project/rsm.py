from collections import defaultdict
from typing import NamedTuple, Dict

from pyformlang.cfg import Variable
from pyformlang.finite_automaton import DeterministicFiniteAutomaton, State
from scipy.sparse import dok_matrix

from project import AdjacencyMatrix


class RSM(NamedTuple):
    start_symbol: Variable
    boxes: Dict[Variable, DeterministicFiniteAutomaton]

    def minimize(self):
        """Minimizes Recursive State Machine.

        :return: Minimized Recursive State Machine.
        """
        return RSM(
            start_symbol=self.start_symbol,
            boxes={v: a.minimize() for v, a in self.boxes.items()},
        )


def build_adjacency_matrix_from_rsm(rsm: RSM) -> AdjacencyMatrix:
    """Builds adjacency matrix from RSM.

    :param rsm: RSM to build from.
    :return: Adjacency matrix.
    """
    states, start_states, final_states = set(), set(), set()
    for nonterm, dfa in rsm.boxes.items():
        for s in dfa.states:
            state = State((nonterm, s.value))
            states.add(state)
            if s in dfa.start_states:
                start_states.add(state)
            if s in dfa.final_states:
                final_states.add(state)
    states = sorted(states, key=lambda s: s.value)
    state_to_idx = {s: i for i, s in enumerate(states)}
    b_mtx = defaultdict(lambda: dok_matrix((len(states), len(states)), dtype=bool))
    for nonterm, dfa in rsm.boxes.items():
        for state_from, transitions in dfa.to_dict().items():
            for label, states_to in transitions.items():
                mtx = b_mtx[label.value]
                states_to = states_to if isinstance(states_to, set) else {states_to}
                for state_to in states_to:
                    mtx[
                        state_to_idx[State((nonterm, state_from.value))],
                        state_to_idx[State((nonterm, state_to.value))],
                    ] = True

    return AdjacencyMatrix(
        state_to_index=state_to_idx,
        start_states=start_states,
        final_states=final_states,
        matrix=b_mtx,
    )
