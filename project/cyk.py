from pyformlang.cfg import CFG


def cyk(word: str, cfg: CFG) -> bool:
    """Checks if a word belongs to a given grammar using CYK algorithm.

    :param word: A word to check.
    :param cfg: Context Free Grammar.
    :return: True if the word belongs to the grammar, False otherwise.
    """
    if len(word) == 0:
        return cfg.generate_epsilon()

    word_length = len(word)
    cnf = cfg.to_normal_form()
    dp = dict()
    for i in range(word_length):
        dp[i] = dict()
        for j in range(word_length):
            dp[i][j] = set()

    length_1 = [prod for prod in cnf.productions if len(prod.body) == 1]
    length_2 = [prod for prod in cnf.productions if len(prod.body) == 2]

    for i, c in enumerate(word):
        for p in length_1:
            if p.body[0].value == c:
                dp[i][i].add(p.head)

    for st in range(1, word_length):
        for i in range(word_length - st):
            j = i + st
            for k in range(i, j):
                other_set = set()
                for p in length_2:
                    if p.body[0] in dp[i][k] and p.body[1] in dp[k + 1][j]:
                        other_set.add(p.head)
                dp[i][j] = dp[i][j] | other_set

    return cfg.start_symbol in dp[0][word_length - 1]


def get_word_from_file(file: str) -> str:
    with open(file) as f:
        return f.read()
