from collections import defaultdict, deque

import operations as op


def init_out(g):
    """
    Computes the number of outgoing edges for each node in the graph g.
    :param g: the graph g.
    :return: a dictionary where keys are nodes and values are the number of outgoing edges of that node.
    """
    out = defaultdict(int)

    for node in g.get_nodes():
        out[node] = len(g.get_successors(node))

    return out


def attractor(g, U, j):
    """
    Computes the attractor for player j of the set U in g. Does not create any strategy and only returns the set that
    corresponds to the attractor.
    :param g: the game graph.
    :param U: the target set.
    :param j: the player for which we compute the attractor.
    :return: W the set of nodes corresponding to the attractor.
    """
    out = init_out(g)  # init out
    queue = deque()  # init queue (deque is part of standard library and allows O(1) append() and pop() at either end)
    # this dictionary is used to know if a node belongs to a winning region without
    # iterating over both winning regions lists (we can check in O(1) in average)
    regions = defaultdict(lambda: -1)
    W = []  # the attractor
    opponent = op.opponent(j)  # player j's opponent

    # for each node in the target set U
    for node in U:
        queue.append(node)  # add node to the end of the queue
        regions[node] = j  # set its regions to j (node is winning for j because reachability objective is satisfied)
        W.append(node)  # add the node to the winning region list of j

    # while queue is not empty
    while queue:
        s = queue.popleft()  # remove and return node on the left side of the queue (first in, first out)

        # iterating over the predecessors of node s
        for sbis in g.get_predecessors(s):
            if regions[sbis] == -1:  # if sbis is not yet visited, its region is -1 by default
                if g.get_node_player(sbis) == j:
                    # belongs to j, set regions and strategy accordingly
                    queue.append(sbis)
                    regions[sbis] = j
                    W.append(sbis)

                elif g.get_node_player(sbis) == opponent:
                    # belongs to j bar, decrement out. If out is 0, set the region accordingly
                    out[sbis] -= 1
                    if out[sbis] == 0:
                        queue.append(sbis)
                        regions[sbis] = j
                        W.append(sbis)

    Wbis = []
    for node in g.get_nodes():
            if regions[node] != j:
                Wbis.append(node)
    return W, Wbis