from collections import deque, defaultdict
from attractors import init_out


def sort_colors_ascending(g):
    return sorted(set([k[1] for k in g.nodes.itervalues()]))


def R_set(g, target_set):
    """
    We compute the attractor of a set of node-priority pairs where the priority
    represents the maximal priority seen so far.
    """
    ascending_priorities = sort_colors_ascending(g)
    v_out = init_out(g)  # a counter for visited edges from each vertex
    out = {(v, p): v_out[v] for v in g.get_nodes()
           for p in ascending_priorities}
    regions = defaultdict(lambda: -1)

    # we keep a queue of newly found winning vertex-priority pairs
    queue = deque(target_set)
    while queue:
        (node, priority) = queue.popleft()
        for pred in g.get_predecessors(node):
            pred_player = g.get_node_player(pred)
            pred_priority = g.get_node_priority(pred)
            if pred_priority > priority:
                continue  # cannot be a predecessor
            if priority > g.get_node_priority(node):
                options = [priority]
            else:
                assert(priority == g.get_node_priority(node))
                options = filter(lambda x: x >= pred_priority and
                                 x <= priority, ascending_priorities)
            for p in options:
                print(str((pred, p)) + "->" + str((node, priority)))
                if regions[(pred, p)] == -1:  # vertex-priority is undecided
                    if pred_player == 0:
                        regions[(pred, p)] = 0
                        if (pred, p) not in target_set:
                            queue.append((pred, p))
                    elif pred_player == 1:
                        out[(pred, p)] -= 1
                        if out[(pred, p)] == 0:
                            regions[(pred, p)] = 0
                            if (pred, p) not in target_set:
                                queue.append((pred, p))
    # prepare output
    W = set()
    complement_W = set()
    for n in g.get_nodes():
        if regions[(n, g.get_node_priority(n))] == 0:
            W.add(n)
        else:
            complement_W.add(n)
    return W, complement_W


def psolC(g, W1, W2):
    node_set = set(g.get_nodes())
    ascending_priorities = sort_colors_ascending(g)
    even_priorities = filter(lambda x: (x % 2) == 0, ascending_priorities)
    T = set([(v, p) for v in node_set for p in even_priorities])
    next_F, _ = R_set(g, T)
    F = set()
    while next_F != F:
        F = next_F
        print("F = " + str(F))
        T = set([(v, p) for v in F for p in even_priorities])
        next_F, _ = R_set(g, T)
        next_F = next_F & F
    W1.extend(F)
    complement = node_set - F
    return g.subgame(complement), W1, W2
