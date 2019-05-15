# -*- coding: utf-8 -*-
from collections import deque, defaultdict

import operations as ops

import buchi.buchi_inter_cobuchi as cobuchi
import buchi.buchi_inter_safety as safety
from attractors import init_out, attractor

DEBUG_PRINT = False


def sort_colors_ascending(g):
    """
    Sort priorities occurring in the game in ascending order of priority.
    :param g:
    :type g: Graph
    :return:
    :rtype:
    """
    # TODO check if this is efficient
    # x is an element of the dictionary (2, (1, 4)) => Node 2, player 1, priority 4
    # we return the node id, sorted by priority incrementally
    return [k[1] for k in sorted(g.nodes.values(), key=lambda x: x[1])]


def monotone_attractor(g, target_set):
    """
    Computes the monotone attractor of the given set of nodes. For details, see the paper 'Fatal Attractors in
    Parity Games: Building Blocks for Partial Solvers'.
    :param g:
    :type g: Graph
    :param target_set:
    :type target_set:
    :return:
    :rtype:
    """
    node = target_set[0]  # every node in the target set has the same priority
    priority = g.get_node_priority(node)  # priority of the node gives us the player for which we compute the attractor
    out = init_out(g)  # init out
    queue = deque()  # init queue (deque is part of standard library and allows O(1) append() and pop() at either end)
    # this dictionary is used to know if a node belongs to a winning region without
    # iterating over both winning regions lists (we can check in O(1) in average)
    regions = defaultdict(lambda: -1)
    W = []  # the attractor
    j = g.get_node_priority(node) % 2  # the player for which we compute the attractor
    opponent = ops.opponent(j)  # player j's opponent

    for node in target_set:
        queue.append(node)  # add node to the end of the queue

    if DEBUG_PRINT:
        print("--- Monotone attractor ---")
        print(g)
        print("Set " + str(target_set) + " Player " + str(j) + " Opponent " + str(opponent) + " Prio " + str(priority))
        print("Marked before start " + str(regions) + " Queue before start " + str(queue))

    # while queue is not empty
    while queue:
        if DEBUG_PRINT: print("     Queue " + str(queue))
        s = queue.popleft()  # remove and return node on the left side of the queue (first in, first out)
        if DEBUG_PRINT: print("     Considering node " + str(s))

        # iterating over the predecessors of node s
        for sbis in g.get_predecessors(s):
            if DEBUG_PRINT:
                print("         Considering predecessor " + str(sbis) + " Is marked ? " + str(
                    regions[sbis]) + "Player " + str(g.get_node_player(sbis)) + " Priority " + str(
                    g.get_node_priority(sbis)))

            if regions[sbis] == -1:  # if sbis is not yet visited, its region is -1 by default

                # if node is the correct player and its priority is lower or equal, add it
                if g.get_node_player(sbis) == j and g.get_node_priority(sbis) <= priority:
                    if DEBUG_PRINT: print("             Predecessor " + str(sbis) + " Added ")

                    # if node has not been considered yet (not already been in the queue) add it
                    # this is to avoid considering the same node twice, which can happen only for the target node and
                    # can mess up the decrementation of the counters for nodes of the opponent
                    if sbis not in target_set:
                        queue.append(sbis)

                    # mark accordingly and add to winning region
                    regions[sbis] = j
                    W.append(sbis)

                # if node is the opposite player and its priority is lower or equal, check its counter of successors
                elif g.get_node_player(sbis) == opponent and g.get_node_priority(sbis) <= priority:

                    # belongs to j bar, decrement out. If out is 0, set the region accordingly
                    out[sbis] -= 1

                    if DEBUG_PRINT: print("             Predecessor " + str(sbis) + " Decrement, new count = " +
                                          str(out[sbis]))

                    if out[sbis] == 0 and g.get_node_priority(sbis) <= priority:

                        if DEBUG_PRINT: print("             Predecessor " + str(sbis) + " Added ")

                        # if node has not been considered yet (not already been in the queue) add it
                        if sbis not in target_set:
                            queue.append(sbis)

                        # mark accordingly and add to winning region
                        regions[sbis] = j
                        W.append(sbis)
    Wbis = []
    for node in g.get_nodes():
        if regions[node] != j:
            Wbis.append(node)
    if DEBUG_PRINT:
        print("Attractor " + str(W) + " Complement " + str(Wbis))
        print("-------------------------\n")

    return W, Wbis


def psolB(g, W1, W2):
    """
    Partial solver psolB for parity games using fatal attractors.
    :param g:
    :type g: Graph
    :return:
    :rtype:
    """

    # TODO check the ascending or descending order used by the algorithm
    for color in sort_colors_ascending(g):

        if DEBUG_PRINT: print("Computing for color " + str(color))

        target_set = ops.i_priority_node(g, color)  # set of nodes of color 'color'

        cache = set()

        # TODO check list comparison efficiency
        while cache != set(target_set) and target_set != []:

            cache = target_set

            MA, rest = monotone_attractor(g, target_set)

            if DEBUG_PRINT: print(" MA " + str(MA) + " Player " + str(g.get_node_player(target_set[0])) + "\n")

            if set(target_set).issubset(MA):

                if DEBUG_PRINT: print("Set " + str(target_set) + " in MA ")

                att, complement = attractor(g, MA, color % 2)

                if color % 2 == 0:
                    W1.extend(att)
                else:
                    W2.extend(att)

                return psolB(g.subgame(complement), W1, W2)

            else:
                target_set = list(set(target_set).intersection(set(MA)))

    return g, W1, W2


def psolB_buchi_cobuchi(g, W1, W2):
    """
    Partial solver psolB for parity games using fatal attractors.
    :param g:
    :type g: Graph
    :return:
    :rtype:
    """
    # TODO check the ascending or descending order used by the algorithm
    for color in sort_colors_ascending(g):

        if DEBUG_PRINT: print("Computing for color " + str(color))

        target_set = ops.i_priority_node(g, color)  # set of nodes of color 'color'

        # TODO here replace previous call by a call which goes through each node and add it to in/out set of color i

        not_target_set_bigger = []
        for node in g.get_nodes():
            if g.get_node_priority(node) > color:
                not_target_set_bigger.append(node)

        # TODO check list comparison efficiency

        w = cobuchi.buchi_inter_cobuchi_player(g, target_set, not_target_set_bigger, color % 2)

        if DEBUG_PRINT: print(" MA " + str(w) + " Player " + str(g.get_node_player(target_set[0])) + "\n")

        if w != []:

            if DEBUG_PRINT: print("Set " + str(target_set) + " in MA ")

            att, complement = attractor(g, w, color % 2)

            if color % 2 == 0:
                W1.extend(att)
            else:
                W2.extend(att)

            return psolB_buchi_cobuchi(g.subgame(complement), W1, W2)

    return g, W1, W2


def psolB_buchi_safety(g, W1, W2):
    """
    Partial solver psolB for parity games using fatal attractors.
    :param g:
    :type g: Graph
    :return:
    :rtype:
    """
    # TODO check the ascending or descending order used by the algorithm
    for color in sort_colors_ascending(g):

        if DEBUG_PRINT: print("Computing for color " + str(color))

        target_set = ops.i_priority_node(g, color)  # set of nodes of color 'color'

        # TODO here replace previous call by a call which goes through each node and add it to in/out set of color i

        not_target_set_bigger = []
        for node in g.get_nodes():
            if g.get_node_priority(node) > color:
                not_target_set_bigger.append(node)

        # TODO check list comparison efficiency

        w = safety.buchi_inter_safety_player(g, target_set, not_target_set_bigger, (color)%2)

        if DEBUG_PRINT: print(" MA " + str(w) + " Player " + str(g.get_node_player(target_set[0])) + "\n")

        if w != []:

            if DEBUG_PRINT: print("Set " + str(target_set) + " in MA ")

            att, complement = attractor(g, w, color % 2)

            if color % 2 == 0:
                W1.extend(att)
            else:
                W2.extend(att)

            return psolB_buchi_safety(g.subgame(complement), W1, W2)

    return g, W1, W2
