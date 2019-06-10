from antichain import Antichain
from graph import Graph

DEBUG_PRINT = False

# TODO careful of aliases on the values, changing one somewhere changing it somewhere else

def psolC_generalized(g, W0, W1):

    # base case : game is empty
    if g.get_nodes() == []:
        if DEBUG_PRINT: print("Base case return")
        return g, W0, W1

    # else retrieve useful information on the game
    nbr_func = g.get_nbr_priority_functions()  # number of functions
    priorities = [[] for z in xrange(nbr_func)]  # setup list containing list of priorities for each function
    even_priorities = [[] for z in xrange(nbr_func)]  # setup list containing list of even priorities for each function
    sizes = [0] * nbr_func  # setup the sizes for the lists of priorities
    even_sizes = [0] * nbr_func  # setup the sizes for the lists of even priorities
    empty_set = set()  # useful when computing fatal attractor for player 1

    # first, retrieve all priorities and put them in the lists of priorities for each function
    for node in g.nodes.iterkeys():
        for func in range(nbr_func):
            priorities[func].append(g.get_node_priority_function_i(node, func + 1))  # function are numbered 1 to k

    # sort priorities and create the lists containing only the even priorities
    for func in range(nbr_func):
        # TODO we transform into set to remove duplicate, might check itertools, ordered dicts and heaps also
        priorities[func] = sorted(set(priorities[func]), reverse=True)  # change into set to remove duplicates and sort
        even_priorities[func] = filter(lambda x: x % 2 == 0, priorities[func])  # keep the sorted even priorities

        # if there are no even priorities according to one of the functions, the game is completely won by player 1
        # return empty game and all nodes added to W2
        if len(even_priorities[func]) == 0:
            W1.extend(g.nodes.keys())
            return Graph(), W0, W1

        sizes[func] = len(priorities[func])
        even_sizes[func] = len(even_priorities[func])

    # here we have sorted lists of priorities as well as their sizes

    indexes = [0] * nbr_func  # index for each function to go trough its priorities
    even_indexes = [0] * nbr_func  # index for each function to go trough its priorities

    if DEBUG_PRINT:
        print("Priorities " + str(priorities))
        print("Sizes " + str(sizes))
        print("Even priorities " + str(even_priorities))
        print("Even sizes " + str(even_sizes))

def truc(g, priorities):
    pass


def intersector(x, y):
    """
    Intersection between two memory values x = m' and y = m.
    """
    parity_x = x % 2
    parity_y = y % 2

    if parity_x == 1:
            if parity_y == 1:
                return min(x, y)
            else:
                return y
    if parity_x == 0:
            if parity_y == 0:
                return max(x, y)
            else:
                return x

def comparator(x, y):
    """
    Comparison between two memory values x = m' and y = m. We want to check whether x <= y
    """
    parity_x = x % 2
    parity_y = y % 2

    if parity_x == 1:
        if parity_y == 1:
            return x <= y
        else:
            return False
    if parity_x == 0:
        if parity_y == 0:
            return x >= y
        else:
            return True


def intersector_generalized(x, y):
    """
    Intersection between two elements [v', m_1', ... m'_k] [v, m_1, ... m_k] is possible iff v = v' (else, elements are
    incomparable and function yields -1). Then we just apply intersection between each memory value.
    """

    if x[0] != y[0]:
        return -1
    else:
        nbr_functions = len(x)
        res = [x[0]]
        for func in range(1, nbr_functions):
            res.append(intersector(x[func], y[func]))

    return res


def comparator_generalized(x, y):
    """
    Comparison between two elements [v', m_1', ... m'_k] [v, m_1, ... m_k] is possible iff v = v' (else, elements are
    incomparable and function yields False). Then we just compare each memory value.
    """

    if x[0] != y[0]:
        return False
    else:
        nbr_functions = len(x)
        for func in range(1, nbr_functions):
            if not comparator(x[func], y[func]):
                return False
    return True


def down_generalized(element, priorities, node, nbr_functions, max_values):
    """
    Computes the largest m = [m_1, ..., m_k] such that up(m, priorities) <= m' = element[1:]. Then we add node to
    obtain [node, m]. When computing down, priorities is a tuple of size k which gives the encountered priority
    according to each priority function. Max_values records the maximum value to know when a memory value is not
    defined.
    """

    # resulting node
    res = [0]*(nbr_functions+1)
    res[0] = node

    # for each priority function (numbered from 1 to k)
    for func in range(1, nbr_functions + 1):

        encountered_priority_p = priorities[func - 1]

        # if priority encountered is even
        if encountered_priority_p % 2 == 0:

            m_prim = element[func]

            if encountered_priority_p < m_prim:
                res[func] = m_prim

            else:
                res[func] = max(encountered_priority_p - 1, 0)

        else:

            m_prim = element[func]

            if encountered_priority_p <= m_prim:
                res[func] = m_prim

            else:

                if encountered_priority_p != max_values[func]:
                    res[func] = encountered_priority_p + 1
                else:
                    return -1

    return res


def create_start_antichain(starting_nodes, nbr_func, even_values):
    # TODO this is a crude creation adding every possibility, we can directly add the max elements io the max
    # even value for each
    start_antichain = Antichain(comparator_generalized, intersector_generalized)

    # create the antichain of maximal elements of the safe set
    # every counter in every tuple has the maximal value
    for node in starting_nodes:
        temp = [0]*(nbr_func + 1)
        temp[0] = node
        for func in range(1, nbr_func+1):
            # even values are sorted
            temp[func] = even_values[func-1][0]
        start_antichain.insert(temp)
    return start_antichain


def compute_fixpoint(graph, starting_nodes, nbr_func, even_values, max_even_values):
    """
    This is the attractor starting node is f_j
    Computes the fixpoint obtained by the symbolic version of the backward algorithm for safety games.
    Starts from the antichain of the safe set and works backwards using controllable predecessors.
    The maximum value for the counters is a parameter to facilitate the incremental algorithm.
    :param graph:
    :type graph:
    :param max_value:
    :type max_value:
    :return:
    :rtype:
    """

    # wether we want to print the sets during computation
    toPrint = False

    # start antichain is antichain of tj
    start_antichain = create_start_antichain(starting_nodes, nbr_func, even_values)

    # TODO change intersection to union, also add target as union when computing cpre, also the true start is
    # the cpre of start

    if (toPrint):
        print("Start antichain : " + str(start_antichain) + "\n")

    antichain1 = start_antichain

    cpre1 = Cpre(start_antichain, 1, graph, nbr_func, max_even_values)

    if (toPrint):
        print("CPre_1 of start antichain: " + str(cpre1) + "\n")

    cpre0 = Cpre(start_antichain, 0, graph, nbr_func, max_even_values)

    if (toPrint):
        print("CPre_0 of start antichain: " + str(cpre0) + "\n")

    # we know the elements of cpre0 and cpre1 to be incomparable. Union of the two antichains can be done through
    # simple extend
    cpre0.incomparable_elements.extend(cpre1.incomparable_elements)

    if (toPrint):
        print("Union of CPre_0 and CPre_1 " + str(cpre0) + "\n")

    antichain2 = antichain1.intersection(cpre0)

    if (toPrint):
        print("Inter of start and previous union " + str(antichain2) + "\n")

    nb_iter = 0

    # while we have not obtained the fixpoint
    while not antichain1.compare(antichain2):

        nb_iter += 1

        antichain1 = antichain2

        cpre1 = Cpre(antichain1, 1, graph, nbr_func, max_even_values)
        if (toPrint):
            print("ITER " + str(nb_iter) + " CPre 1 of prev " + str(cpre1) + "\n")

        cpre0 = Cpre(antichain1, 0, graph, nbr_func, max_even_values)

        if (toPrint):
            print("ITER " + str(nb_iter) + " CPre 0 of prev " + str(cpre0) + "\n")

        temp = cpre0.union(cpre1)

        if (toPrint):
            print("ITER " + str(nb_iter) + " Union of Pre 0 and Pre 1  " + str(temp) + "\n")

        antichain2 = antichain1.intersection(temp)

        if (toPrint):
            print("ITER " + str(nb_iter) + " final set  " + str(antichain2) + "\n")

    return antichain1


def Cpre(antichain, player, graph, nbr_functions, max_value):
    """
    Calls the correct controllable predecessor function depending on the player.
    :param antichain:
    :type antichain:
    :param player:
    :type player:
    :param graph:
    :type graph:
    :param nbr_functions:
    :type nbr_functions:
    :param max_value:
    :type max_value:
    :return:
    :rtype:
    """
    if player == 0:
        return Cpre_0(antichain, graph, nbr_functions, max_value)
    else:
        return Cpre_1(antichain, graph, nbr_functions, max_value)


def Cpre_1(antichain, graph, nbr_functions, max_value):
    """
    Computes the antichain of the controllable predecessors for player 1 of 'antichain'.
    :param antichain:
    :type antichain:
    :param graph:
    :type graph:
    :param nbr_functions:
    :type nbr_functions:
    :param max_value:
    :type max_value:
    :return:
    :rtype:
    """

    if antichain.incomparable_elements == []:
        return antichain

    cur_antichain = Antichain(comparator_generalized, intersector_generalized)
    for node in graph.get_nodes():
        if graph.get_node_player(node) == 1:
            first_iteration = True
            temp2 = Antichain(comparator_generalized, intersector_generalized)  # contains the set for intersection
            for succ in graph.get_successors(node):
                temp1 = Antichain(comparator_generalized, intersector_generalized)
                for element in antichain.incomparable_elements:
                    if element[0] == succ:

                        computed_down = down_generalized(element, graph.nodes[node][1:], node, nbr_functions, max_value)
                        # print("Down = "+str(computed_down)+" Compute down of "+str(element)+" with prio "+str(graph.get_node_priority(node))+" node "+str(node)+" val max "+str(max_counter))

                        if computed_down != -1:
                            temp1.insert(computed_down)

                if first_iteration:
                    temp2 = temp1
                    first_iteration = False
                else:
                    # print("temp1 "+str(temp1)+ " temp2 "+str(temp2))
                    temp2 = temp1.intersection(temp2)
                    # print("inter  "+str(temp2))

            cur_antichain = cur_antichain.union(temp2)

    return cur_antichain


def Cpre_0(antichain, graph, nbr_functions, max_value):
    """
    Computes the antichain of the controllable predecessors for player 0 of 'antichain'.
    :param antichain:
    :type antichain:
    :param graph:
    :type graph:
    :param nbr_functions:
    :type nbr_functions:
    :param max_value:
    :type max_value:
    :return:
    :rtype:
    """

    if antichain.incomparable_elements == []:
        return antichain

    cur_antichain = Antichain(comparator_generalized, intersector_generalized)
    for element in antichain.incomparable_elements:
        for pred in graph.get_predecessors(element[0]):
            if graph.get_node_player(pred) == 0:
                computed_down = down_generalized(element, graph.nodes[pred][1:], pred, nbr_functions,
                                                   max_value)
                if computed_down != -1:
                    cur_antichain.insert(computed_down)

    return cur_antichain

"""
import file_handler as io
g = io.load_generalized_from_file("generalized_parity_game_example.txt")
fixpoint = compute_fixpoint_0(g, 4)
print("Fixpoint : " + str(fixpoint))
# solution should be [1, 2] and [3,4,5]
"""