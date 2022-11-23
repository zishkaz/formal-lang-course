from collections import deque, defaultdict
from typing import Union, Set

from networkx import MultiDiGraph
from pyformlang.cfg import CFG, Variable, Terminal
from scipy.sparse import dok_matrix

from project import load_graph, get_cfg_from_file, cfg_to_weak_cnf


def run_hellings_algo(cfg: CFG, graph: MultiDiGraph) -> Set:
    """Runs Hellings algorithm on the given Context Free Grammar and graph.

    :param cfg: Context Free Grammar.
    :param graph: Graph.
    :return: Set of Triples [vertex, variable, vertex]. It means that two variables have path between them that
    was received from the specified CFG variable.
    """

    node_count = graph.number_of_nodes()
    if node_count == 0:
        return set()

    weak_cnf = cfg_to_weak_cnf(cfg)
    terminal_to_variable = defaultdict(set)
    pair_variables_to_variable = defaultdict(set)
    epsilon_variables = set()

    for p in weak_cnf.productions:
        head, body = p.head, p.body
        body_len = len(body)
        if body_len == 0:
            epsilon_variables.add(head)
        elif body_len == 1:
            terminal_to_variable[head].add(body[0])
        elif body_len == 2:
            pair_variables_to_variable[head].add((body[0], body[1]))

    result = set()
    for node in graph.nodes:
        for var in epsilon_variables:
            result.add((node, var, node))
    for i, j, label in graph.edges(data="label"):
        for n, terms in terminal_to_variable.items():
            if Terminal(label) in terms:
                result.add((i, n, j))

    dq = deque(result.copy())

    while len(dq) > 0:
        i, var1, j = dq.popleft()
        sub_res = set()
        for u, var2, v in result:
            if v == i:
                for node_count, var_to_var in pair_variables_to_variable.items():
                    new = (u, node_count, j)
                    if (var2, var1) in var_to_var and new not in result:
                        dq.append(new)
                        sub_res.add(new)
            if j == u:
                for node_count, var_to_var in pair_variables_to_variable.items():
                    new = (i, node_count, v)
                    if (var1, var2) in var_to_var and new not in result:
                        dq.append(new)
                        sub_res.add(new)
        result = result.union(sub_res)

    return result


def run_matrix_algo(cfg: CFG, graph: MultiDiGraph) -> Set:
    """Runs Matrix algorithm on the given Context Free Grammar and graph.

    :param cfg: Context Free Grammar.
    :param graph: Graph.
    :return: Set of Triples [vertex, variable, vertex]. It means that two variables have path between them that
    was received from the specified CFG variable.
    """
    node_count = graph.number_of_nodes()
    if node_count == 0:
        return set()

    nodes = list(graph.nodes)
    node_to_index = defaultdict(int)
    for i, node in enumerate(nodes):
        node_to_index[i] = node

    weak_cnf = cfg_to_weak_cnf(cfg)
    terminal_to_variable = defaultdict(set)
    pair_variables_to_variable = defaultdict(set)
    epsilon_variables = set()
    for p in weak_cnf.productions:
        head, body = p.head, p.body
        body_len = len(body)
        if body_len == 0:
            epsilon_variables.add(head)
        elif body_len == 1:
            terminal_to_variable[head].add(body[0])
        elif body_len == 2:
            pair_variables_to_variable[head].add((body[0], body[1]))

    var_to_matrix = defaultdict(dok_matrix)
    for var in weak_cnf.variables:
        var_to_matrix[var] = dok_matrix((node_count, node_count), dtype=bool)

    for i in range(node_count):
        for node_count in epsilon_variables:
            var_to_matrix[node_count][i, i] = True

    for i_node, j_node, label in graph.edges(data="label"):
        i, j = node_to_index[i_node], node_to_index[j_node]
        for node_count, terms in terminal_to_variable.items():
            if Terminal(label) in terms:
                var_to_matrix[node_count][i, j] = True

    while True:
        changed = False
        for node_count, var_to_var in pair_variables_to_variable.items():
            old_nnz = var_to_matrix[node_count].nnz
            var_to_matrix[node_count] += sum(
                var_to_matrix[n1] @ var_to_matrix[n2] for n1, n2 in var_to_var
            )
            changed |= old_nnz != var_to_matrix[node_count].nnz
        if changed is False:
            break

    result = set()
    for var, matrix in var_to_matrix.items():
        for i, j in zip(*matrix.nonzero()):
            result.add((nodes[i], var, nodes[j]))
    return result


algo_map = {"hellings": run_hellings_algo, "matrix": run_matrix_algo}


def run_cfpq(
        algo: str,
        graph: Union[str, MultiDiGraph],
        cfg: Union[str, CFG],
        start_nodes: Set = None,
        final_nodes: Set = None,
        start_symbol: Variable = Variable("S"),
) -> Set:
    """Executes query on graph with Hellings algorithm.

    :param algo: String name of the algorithm to use for CFPQ. Currently supports "hellings" and "matrix".
    :param graph: Given graph, as name from cfpq-data dataset, or graph itself as MultiDiGraph.
    :param cfg: File path containing Context Free Grammar, or Context Free Grammar instead.
    :param start_nodes: Set of graph start nodes. Defaults to all nodes being start nodes.
    :param final_nodes: Set of graph final nodes. Defaults to all nodes being final nodes.
    :param start_symbol: Start symbol of the given grammar. Defaults to "S".
    :return: Pairs of vertices that have path between them with given constraints from graph.
    """

    if isinstance(graph, str):
        graph = load_graph(graph)
    if isinstance(cfg, str):
        cfg = get_cfg_from_file(cfg)
    cfg._start_symbol = start_symbol
    if start_nodes is None:
        start_nodes = graph.nodes
    if final_nodes is None:
        final_nodes = graph.nodes
    result_set = set()
    for (i, k, j) in algo_map[algo](cfg, graph):
        if start_symbol == k and i in start_nodes and j in final_nodes:
            result_set.add((i, j))
    return result_set
