from project import convert_ecfg_to_rsm, regex_to_min_dfa, get_ecfg_from_text


def check(ecfg, rsm):
    assert all(
        regex_to_min_dfa(ecfg.productions[v]).is_equivalent_to(rsm.boxes[v].minimize())
        for v in ecfg.productions
    )


def test_convert_ecfg_to_rsm_1():
    ecfg_as_text = "S -> x"
    ecfg = get_ecfg_from_text(ecfg_as_text)
    rsm = convert_ecfg_to_rsm(ecfg)
    check(ecfg, rsm)


def test_convert_ecfg_to_rsm_2():
    ecfg_as_text = "S -> b|S*"
    ecfg = get_ecfg_from_text(ecfg_as_text)
    rsm = convert_ecfg_to_rsm(ecfg)
    check(ecfg, rsm)


def test_convert_ecfg_to_rsm_3():
    ecfg_as_text = "S -> (a) | (b* S)"
    ecfg = get_ecfg_from_text(ecfg_as_text)
    rsm = convert_ecfg_to_rsm(ecfg)
    check(ecfg, rsm)
