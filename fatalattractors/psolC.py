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
                continue
            for p in ascending_priorities:
                if p < pred_priority:
                    continue  # impossiburu
                elif p > priority:
                    break  # will never reach (node, priority)
                if regions[(pred, p)] == -1:  # vertex-priority is undecided
                    if pred_player == 0:
                        regions[(pred, p)] = 0
                        queue.append((pred, p))
                    elif pred_player == 1:
                        out[(pred, p)] -= 1
                        if out[(pred, p)] == 0:
                            regions[(pred, p)] = 0
                            queue.append((pred, p))
    # prepare output
    W = []
    complement_W = []
    for n in g.get_nodes():
        if regions[(n, g.get_node_priority(n))] == 0:
            W.append(n)
        else:
            complement_W.append(n)
    return W, complement_W
