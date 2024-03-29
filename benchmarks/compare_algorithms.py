import sys
import copy
import signal
import pickle
import matplotlib.pyplot as plt
import operations as ops
import timer


TIMEOUT = 60


def set_timeout(t):
    global TIMEOUT
    TIMEOUT = t


class TimeoutException(Exception):
    pass


def handler(signum, frame):
    raise TimeoutException("Timeout!")


def compare_complete_algorithms_LTLbenchmarks(algorithms, generator, n,
                                              preprocess=None, iterations=3,
                                              step=10, check_solution=False,
                                              plot=False, path=" ",
                                              path_tot=" ", title="plot",
                                              labels=None, pkl_path=""):
    """
    Compares the running time of so called complete algorithms for parity or generalized parity games.
    This implementation is specific to LTL benchmarks as it sorts the points before plotting them.
    :param algorithms: list of algorithms.
    :param generator: generator to create the games on which to run these algorithms.
    :param n: maximum parameter for the generator.
    :param preprocess: a pre-processing algorithm to apply on the game graphs (usually priority compression).
    :param iterations: the number of times the solving time is recorded (minimum time is chosen).
    :param step: the step used for the parameter of the generator.
    :param check_solution: an algorithm to check the solutions computed for control purposes (a complete solver for the
    given game).
    :param plot: whether to plot the result.
    :param path: path for the plot.
    :param title: title for the plot.
    :param labels: labels for the plot (name of each algorithm).
    """

    number_of_algorithms = len(algorithms)

    y = [[] for z in xrange(number_of_algorithms)]
    x = []
    game_parameters = []

    chrono = timer.Timer(verbose=False)  # Timer object

    # Games generated are size 5 to n using the specified step
    for i in range(0, n, step):
        sys.stdout.flush()

        # if check_solution, we will verify the solutions are the same across the different algorithms
        if check_solution:
            winning_player_1 = []
            winning_player_2 = []

        recordings = [[0] * iterations for z in xrange(number_of_algorithms)]

        g = generator(i)  # game generation
        x.append(len(g.get_nodes()))
        print("Experiments on benchmark no. " + str(i))
        game_parameters.append((g.name,
                                len(g.get_nodes()),
                                g.get_nbr_priorities()))

        for k in range(number_of_algorithms):
            g_copy = copy.deepcopy(g)

            if preprocess[k] is not None:
                g_copy = preprocess[k](g_copy)

            # #iterations calls to the solver are timed
            for j in range(iterations):
                # failed = False
                signal.signal(signal.SIGALRM, handler)
                signal.alarm(TIMEOUT)
                with chrono:
                    try:
                        W1, W2 = algorithms[k](g_copy)  # solver call
                    except TimeoutException:
                        # failed = True
                        print("Algorithm " + str(k) +
                              " just timed out, benchmark " + str(i))
                        W1, W2 = [], []  # probably a timeout
                signal.alarm(0)

                # if not failed:
                recordings[k][j] = chrono.interval

            # if min(recordings[k]) == 0:
            #     y[k].append(TIMEOUT)  # get the minimum out of #iterations recordings
            # else:
            min_recording = min(recordings[k])
            y[k].append(min_recording)  # get the minimum out of #iterations recordings

            # algorithms should not modify the original game arena
            assert (len(g.get_nodes()) == len(g_copy.get_nodes()))

            if check_solution:
                # algorithms are deterministic so we only record the last solution
                winning_player_1.append(W1)
                winning_player_2.append(W2)

        if check_solution:
            for u in range(number_of_algorithms - 1):
                assert (ops.are_lists_equal(winning_player_1[u], winning_player_1[u + 1]))
                assert (ops.are_lists_equal(winning_player_2[u], winning_player_2[u + 1]))

    # just in case, we also save a pickle file
    if pkl_path:
        xy_pkl = open(pkl_path, 'wb')
        pickle.dump((game_parameters, x, y), xy_pkl)
        xy_pkl.close()

    if plot:
        plt.grid(True)
        plt.title(title)
        plt.xlabel(u'number of nodes')
        plt.ylabel(u'time (s)')

        colors = ['-g.', '-r.', '-b.', '-y.', '-c.', '-k.', '-m.']
        plt.xscale("log")
        plt.yscale("log")
        from matplotlib.font_manager import FontProperties

        fontP = FontProperties()
        fontP.set_size('small')

        points = []
        for i in range(number_of_algorithms):
            x_cop, y_cop = (list(t) for t in
                            zip(*sorted(zip(x, y[i]))))  # sorting points
            points.extend(plt.plot(x_cop, y_cop, colors[i], label=labels[i]))

        plt.legend(loc='upper left', handles=points, prop=fontP)
        plt.savefig(path, bbox_inches='tight')
        plt.clf()
        plt.close()

        # we need to compute how many benchmarks there are
        bench_count = range(1, len(x) + 1)
        # now we need to sort the running times of the algorithms in increasing order
        # and add them
        sorted_times = [sorted(y[i]) for i in range(len(y))]
        tot_solve_times = []
        for i in range(len(y)):
            cst = []
            total_time = 0
            for j in range(len(x)):
                total_time += sorted_times[i][j]
                cst.append(total_time)
            tot_solve_times.append(cst)

        plt.grid(True)
        plt.title("Cumulative time graph")
        plt.xlabel(u'no. of benchmarks')
        plt.ylabel(u'total time spent')
        plt.yscale("log")  # allows logatithmic y-axis

        colors = ['-g.', '-r.', '-b.', '-y.', '-c.', '-k.', '-m.']

        points = []
        for i in range(number_of_algorithms):
            points.extend(plt.plot(bench_count, tot_solve_times[i],
                                   colors[i], label=labels[i]))

        plt.legend(loc='lower right', handles=points)
        plt.savefig(path_tot, bbox_inches='tight')
        plt.clf()
        plt.close()

    """
    if plot:
        plt.grid(True)
        plt.title(title)
        plt.xlabel(u'number of nodes')
        plt.ylabel(u'time (s)')

        colors = ['-g.', '-r.', '-b.', '-y.', '-c.', '-k.', '-m.']
        # plt.yscale("log") allows logatithmic y-axis

        points = []
        for i in range(number_of_algorithms):
            points.extend(plt.plot(x, y[i], colors[i], label=labels[i]))

        plt.legend(loc='upper left', handles=points)
        plt.savefig(path, bbox_inches='tight')
        plt.clf()
        plt.close()
    """


def compare_complete_algorithms(algorithms, generator, n, preprocess=None, iterations=3, step=10, check_solution=False,
                                plot=False, path=" ", title="plot", labels=None):
    """
    Compares the running time of so called complete algorithms for parity or generalized parity games.

    :param algorithms: list of algorithms.
    :param generator: generator to create the games on which to run these algorithms.
    :param n: maximum parameter for the generator.
    :param preprocess: a pre-processing algorithm to apply on the game graphs (usually priority compression).
    :param iterations: the number of times the solving time is recorded (minimum time is chosen).
    :param step: the step used for the parameter of the generator.
    :param check_solution: an algorithm to check the solutions computed for control purposes (a complete solver for the
    given game).
    :param plot: whether to plot the result.
    :param path: path for the plot.
    :param title: title for the plot.
    :param labels: labels for the plot (name of each algorithm).
    """

    number_of_algorithms = len(algorithms)

    y = [[] for z in xrange(number_of_algorithms)]
    x = []

    chrono = timer.Timer(verbose=False)  # Timer object

    # Games generated are size 5 to n using the specified step
    for i in range(1, n + 1, step):
        sys.stdout.flush()

        # if check_solution, we will verify the solutions are the same across the different algorithms
        if check_solution:
            winning_player_1 = []
            winning_player_2 = []

        recordings = [[0] * iterations for z in xrange(number_of_algorithms)]

        g = generator(i)  # game generation
        x.append(len(g.get_nodes()))

        for k in range(number_of_algorithms):
            g_copy = copy.deepcopy(g)

            if preprocess[k] is not None:
                g_copy = preprocess[k](g_copy)

            # #iterations calls to the solver are timed
            for j in range(iterations):
                signal.signal(signal.SIGALRM, handler)
                signal.alarm(TIMEOUT)
                with chrono:
                    try:
                        W1, W2 = algorithms[k](g_copy)  # solver call
                    except TimeoutException:
                        print("Algorithm " + str(k) + " just timed out")
                        W1, W2 = [], []  # probably a timeout
                signal.alarm(0)

                recordings[k][j] = chrono.interval

            min_recording = min(recordings[k])

            y[k].append(min_recording)  # get the minimum out of #iterations recordings

            # algorithms should not modify the original game arena
            assert (len(g.get_nodes()) == len(g_copy.get_nodes()))

            if check_solution:
                # algorithms are deterministic so we only record the last solution
                winning_player_1.append(W1)
                winning_player_2.append(W2)

        if check_solution:
            for u in range(number_of_algorithms - 1):
                assert (ops.are_lists_equal(winning_player_1[u], winning_player_1[u + 1]))
                assert (ops.are_lists_equal(winning_player_2[u], winning_player_2[u + 1]))

    if plot:
        plt.grid(True)
        plt.title(title)
        plt.xlabel(u'number of nodes')
        plt.ylabel(u'time (s)')

        colors = ['-g.', '-r.', '-b.', '-y.', '-c.']
        # plt.yscale("log") allows logatithmic y-axis

        points = []
        for i in range(number_of_algorithms):
            points.extend(plt.plot(x, y[i], colors[i], label=labels[i]))

        plt.legend(loc='upper left', handles=points)
        plt.savefig(path, bbox_inches='tight')
        plt.clf()
        plt.close()


def compare_partial_algorithms(algorithms, generator, n, preprocess=None,
                               iterations=3, step=10, control_algorithm=None,
                               plot=False, path_time=" ", path_proportion=" ",
                               path_bulkprop=" ", path_tottime=" ",
                               title="plot", labels=None, pkl_path=""):
    """
    Compares the running time of so called partial algorithms for parity or generalized parity games.
    This compares the running time as well as the proportion of the game which is solved.

    :param algorithms: list of algorithms.
    :param generator: generator to create the games on which to run these algorithms.
    :param n: maximum parameter for the generator.
    :param preprocess: a pre-processing algorithm to apply on the game graphs (usually priority compression).
    :param iterations: the number of times the solving time is recorded (minimum time is chosen).
    :param step: the step used for the parameter of the generator.
    :param control_algorithm: an algorithm to check if the partial solutions computed are included in the actual
    solution, for control purposes (must provide a complete solver for the given game).
    :param plot: whether to plot the result.
    :param path_time: path for the plot recording the running time comparison.
    :param path_proportion: path for the plot recording the proportion solved comparison.
    :param title: title for the plot.
    :param labels: labels for the plot (name of each algorithm).
    """

    number_of_algorithms = len(algorithms)

    y = [[] for t in xrange(number_of_algorithms)]
    z = [[] for t in xrange(number_of_algorithms)]
    x = []
    game_parameters = []

    chrono = timer.Timer(verbose=False)  # Timer object

    for i in range(0, n, step):
        sys.stdout.flush()

        # if check_solution, we will verify the solutions are the same across the different algorithms
        if control_algorithm:
            winning_player_1 = []
            winning_player_2 = []

        recordings = [[0] * iterations for t in xrange(number_of_algorithms)]

        g = generator(i)  # game generation
        game_parameters.append((g.name,
                                len(g.get_nodes()),
                                g.get_nbr_priorities()))

        x.append(len(g.get_nodes()))
        print("Experiments on benchmark no. " + str(i))

        for k in range(number_of_algorithms):
            g_copy = copy.deepcopy(g)

            if preprocess[k] is not None:
                g_copy = preprocess[k](g_copy)

            # #iterations calls to the solver are timed
            for j in range(iterations):
                # g_copy = copy.deepcopy(g)  # TODO is this required
                signal.signal(signal.SIGALRM, handler)
                signal.alarm(TIMEOUT)
                with chrono:
                    try:
                        rest, W1, W2 = algorithms[k](g_copy, [], [])  # solver call
                    except TimeoutException:
                        print("Algorithm " + str(k) + " just timed out")
                        rest, W1, W2 = g, [], []  # probably a timeout
                signal.alarm(0)

                recordings[k][j] = chrono.interval

            min_recording = min(recordings[k])
            y[k].append(min_recording)  # get the minimum out of #iterations recordings

            # algorithms should not modify the original game arena
            assert (len(g.get_nodes()) == len(g_copy.get_nodes()))

            if control_algorithm:
                winning_player_1.append(W1)
                winning_player_2.append(W2)

            # get the percentage of the arena which is solved
            z[k].append(((len(g.get_nodes()) - len(rest.get_nodes())) / float(len(g.get_nodes()))) * 100)

        if control_algorithm:
            print("Running the control algorithm")
            signal.signal(signal.SIGALRM, handler)
            signal.alarm(TIMEOUT)
            try:
                expected_1, expected_2 = control_algorithm(g_copy)
                for u in range(number_of_algorithms):
                    '''
                    print("CURRENT ALGORITHM " + str(u))
                    print(winning_player_2[u])
                    print(expected_2)
                    print(winning_player_1[u])
                    print(expected_1)
                    '''
                    assert (set(winning_player_2[u]).issubset(expected_2))
                    assert (set(winning_player_1[u]).issubset(expected_1))
            except TimeoutException:
                print("The control algorithm timed out")
            finally:
                signal.alarm(0)

    # just in case, we also save a pickle file
    if pkl_path:
        xyz_pkl = open(pkl_path, 'wb')
        pickle.dump((game_parameters, x, y, z), xyz_pkl)
        xyz_pkl.close()

    if plot:
        plt.grid(True)
        plt.title(title)
        plt.xlabel(u'number of nodes')
        plt.ylabel(u'time (s)')

        colors = ['g.', 'r.', 'b.', 'y.', 'c.']
        # plt.yscale("log") allows logatithmic y-axis

        points = []
        for i in range(number_of_algorithms):
            points.extend(plt.plot(x, y[i], colors[i], label=labels[i]))

        plt.legend(loc='upper left', handles=points)
        plt.savefig(path_time, bbox_inches='tight')
        plt.clf()
        plt.close()

        plt.grid(True)
        plt.title(title)
        plt.xlabel(u'number of nodes')
        plt.ylabel(u'percentage of the game solved')

        # plt.yscale("log") allows logatithmic y-axis

        points = []
        for i in range(number_of_algorithms):
            points.extend(plt.plot(x, z[i], colors[i], label=labels[i]))

        plt.legend(loc='upper left', handles=points)
        plt.savefig(path_proportion, bbox_inches='tight')
        plt.clf()
        plt.close()

        class_pct = range(5, 105, 5)

        plt.grid(True)
        plt.title("Benchmark node classification")
        plt.xlabel(u'classification %')
        plt.ylabel(u'no. of benchmarks')

        colors = ['g.', 'r.', 'b.', 'y.', 'c.']

        points = []
        for i in range(number_of_algorithms):
            vals = []
            for p in class_pct:
                vals.append(sum([1 if v >= p else 0
                                 for v in z[i]]))
            points.extend(plt.plot(class_pct, vals, colors[i], label=labels[i]))

        plt.legend(loc='lower left', handles=points)
        plt.savefig(path_bulkprop, bbox_inches='tight')
        plt.clf()
        plt.close()

        # we need to compute how many benchmarks there are
        bench_count = range(1, len(x) + 1)
        # now we need to sort the running times of the algorithms in increasing order
        # and add them
        sorted_times = [sorted(y[i]) for i in range(len(y))]
        tot_solve_times = []
        for i in range(len(y)):
            cst = []
            total_time = 0
            for j in range(len(x)):
                total_time += sorted_times[i][j]
                cst.append(total_time)
            tot_solve_times.append(cst)

        plt.grid(True)
        plt.title("Cumulative time graph")
        plt.xlabel(u'no. of benchmarks')
        plt.ylabel(u'total time spent')
        plt.yscale("log")  # allows logatithmic y-axis

        colors = ['g.', 'r.', 'b.', 'y.', 'c.']

        points = []
        for i in range(number_of_algorithms):
            points.extend(plt.plot(bench_count, tot_solve_times[i],
                          colors[i], label=labels[i]))

        plt.legend(loc='lower right', handles=points)
        plt.savefig(path_tottime, bbox_inches='tight')
        plt.clf()
        plt.close()


"""
# Example of usage.
# If random games need to be generated for comparison, use a wrapper
function such as

import zielonka as zie
import fatalattractors.psol as psol
import fatalattractors.psolB as psolB
import fatalattractors.psolQ as psolQ

import generators as gene


def gen(i):
    return gene.random(i, i, 1, i / 3)


algorithms_complete = [zie.strong_parity_solver_no_strategies, zie.zielonka_with_psolB,
                       zie.zielonka_with_psolB_buchi_safety, zie.zielonka_with_psolB_buchi_cobuchi]

compare_complete_algorithms(algorithms_complete, gen, 500, preprocess=[None, None, None, None], iterations=3, step=10,
                            check_solution=True, plot=True,
                            path="compare_complete_ziel_zielPSOLB_zielPSOLBuchi-safety_zielPSOLBuchi-coBuchi.pdf",
                            title="Comparison of complete solvers for parity games",
                            labels=["Ziel", "Ziel + PSOLB", "Ziel + PSOLB Buchi-safety", "Ziel + PSOLB Buchi-coBuchi"])

algorithms_partial = [psol.psol, psolB.psolB, psolB.psolB_buchi_safety, psolQ.psolQ, psolQ.psolQ_buchi]

compare_partial_algorithms(algorithms_partial, gen, 500, preprocess=[None,
    None, None, None, None], iterations=3, step=10,
    control_algorithm=zie.strong_parity_solver_no_strategies, plot=True,
    path_time="compare_partials_time.pdf",
    path_proportion="compare_partials_proportion.pdf", title="Comparison of
    partial solvers for parity games", labels=["psol", " psolB", " psolB
    Buchi-safety", "psolQ", "psolQ vero"])
"""
