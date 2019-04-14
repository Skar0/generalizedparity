import copy

from fatalattractors import attractors as reachability
import operations as ops


def transform_game(g, k):
    """
    Transforms a game as a pre-processing to the generalized parity games solver.
    Every priority function is "complemented" (each priority is incremented by 1)
    :param g: the game to complement
    :param k:
    :return: the compemented game
    """
    g_copy = copy.deepcopy(g)  # Deep copy of the game g
    descriptors = g_copy.get_nodes_descriptors()  # Descriptors of the nodes (player, priority_1, ..., priority_k)
    # For each node, get the descriptor and update the descriptor by adding 1 to each priority
    for node in g_copy.get_nodes():
        current = descriptors[node]
        descriptors[node] = tuple([current[0]] + map(lambda x: x + 1, current[1:]))
    return g_copy


def disj_parity_win(g, maxValues, k, u):
    """
    Recursive solver for generalized parity games. Implements the classical algorithm which solves generalized parity
    games.
    :param g: the game to solve
    :param maxValues: the maximum value according to each priority function
    :param k: the number of priority functions
    :param u: integer for testing purposes
    :return: W1, W2 the winning regions in the game for player 1 and player 2 (for the original game, without complement)
    """

    # Base case : all maxValues are 1 or the game is empty
    if all(value == 1 for value in maxValues) or len(g.nodes) == 0:
        return g.get_nodes(), []

    # I added this condition, which states that if there is only one node left with only odd priorities, it is winning
    # for player 1 (since we work with complemented priorities in this algorithm)
    """
    if len(g.nodes) == 1 and all(value%2 == 1 for value in g.nodes[g.get_nodes()[0]][1:]):
        return g.get_nodes(), []
    """

    for i in range(k):

        attMaxOdd, compl_attMaxOdd = reachability.attractor(g, ops.i_priority_node_function_j(g, maxValues[i], i + 1),
                                                            0)
        G1 = g.subgame(compl_attMaxOdd)
        attMaxEven, compl_attMaxEven = reachability.attractor(G1, ops.i_priority_node_function_j(G1, maxValues[i] - 1,
                                                                                                 i + 1), 1)
        H1 = G1.subgame(compl_attMaxEven)
        j = 0
        while True:
            j += 1
            copy_maxValues = copy.copy(maxValues)
            copy_maxValues[i] -= 2
            W1, W2 = disj_parity_win(H1, copy_maxValues, k, u + 1)

            if len(G1.nodes) == 0:
                break

            if set(W2) == set(H1.get_nodes()):
                B, compl_B = reachability.attractor(g, G1.get_nodes(), 1)
                W1, W2 = disj_parity_win(g.subgame(compl_B), maxValues, k, u + 1)
                B.extend(W2)
                return W1, B

            T, compl_T = reachability.attractor(G1, W1, 0)
            G1 = G1.subgame(compl_T)
            E, compl_E = reachability.attractor(G1, ops.i_priority_node_function_j(g, maxValues[i] - 1, i + 1), 0)
            H1 = G1.subgame(compl_E)
    return g.get_nodes(), []


def generalized_parity_solver(g):
    """
    Generalized parity games solver. This is an implementation of the classical algorithm used to solve generalized
    parity games. This is the wrapper function which complements every priority and calls the actual algorithm.
    :param g: the arena of the generalized parity game
    :return: the solution in the following format : W_0, W_1
    """
    # nbr of functions is the length of the descriptor minus 1 (because the descriptor contains the player)
    nbrFunctions = len(g.get_nodes_descriptors()[g.get_nodes()[0]]) - 1
    # Transforming the game
    transformed = transform_game(g, nbrFunctions)
    # Initializing the max values list
    maxValues = [0] * nbrFunctions

    # Getting the maximum value according to each priority function
    descriptors = transformed.get_nodes_descriptors()

    # Get the maximal priority in the game according to every priority function.
    for node in transformed.get_nodes():
        current = descriptors[node]
        for i in range(1, nbrFunctions + 1):
            if current[i] > maxValues[i - 1]:
                maxValues[i - 1] = current[i]

    # Max values need to be odd, if some are even, add 1
    for i in range(0, nbrFunctions):
        if maxValues[i] % 2 == 0:
            maxValues[i] += 1

    return disj_parity_win(transformed, maxValues, nbrFunctions, 0)


"""
import file_handler as io
g = io.load_generalized_from_file("examples/seed_72-10,4,10,1,10.txt")
W1, W2 = generalized_parity_solver(g)
"""
