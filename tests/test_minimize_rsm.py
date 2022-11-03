from project import get_ecfg_from_text, convert_ecfg_to_rsm


def check(minimized_rsm):
    assert all(
        automaton.is_equivalent_to(automaton.minimize())
        for automaton in minimized_rsm.boxes.values()
    )


def test_minimize_rsm_1():
    ecfg_as_text = ""
    rsm = convert_ecfg_to_rsm(get_ecfg_from_text(ecfg_as_text))
    minimized = rsm.minimize()
    check(minimized)


def test_minimize_rsm_2():
    ecfg_as_text = "S -> x"
    rsm = convert_ecfg_to_rsm(get_ecfg_from_text(ecfg_as_text))
    minimized = rsm.minimize()
    check(minimized)


def test_minimize_rsm_3():
    ecfg_as_text = "S -> (a) | (b* S)"
    rsm = convert_ecfg_to_rsm(get_ecfg_from_text(ecfg_as_text))
    minimized = rsm.minimize()
    check(minimized)
