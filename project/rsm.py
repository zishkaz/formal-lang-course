from typing import NamedTuple, Dict

from pyformlang.cfg import Variable
from pyformlang.finite_automaton import DeterministicFiniteAutomaton


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
