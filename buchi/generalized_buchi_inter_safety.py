from buchi.generalized_buchi import generalized_buchi_classical
from fatalattractors import attractors

def generalized_buchi_inter_safety(g, sets, s):
    """
    Solves a generalized Buchi inter safety game where player 0 has that objective.
    sets contains the sets to be visited infinitely often
    and s is to be avoided.
    :param g: a game graph.
    :param sets: the sets of nodes to be visited infinitely often.
    :param s: the set of nodes to be avoid.
    :return: the winning regions w_0, w_1.
    """

    a, not_a = attractors.attractor(g, s, 1)
    g_reduced = g.subgame(not_a)
    return generalized_buchi_classical(g_reduced, sets)