#!/usr/bin/env python


import zielonka
import generators
import tlsf_generators
import fatalattractors.psol as psol
import fatalattractors.psolB as psolB
from benchmarks.compare_algorithms import compare_partial_algorithms


def random_games(i):
    # for some reason this does not work for indices < 5
    j = i + 5
    return generators.random(j, j, 1, j / 3)


def main():
    algorithms_partial = [psol.psol,
                          psolB.psolB,
                          psolB.psolB_buchi_safety,
                          psolB.psolB_buchi_cobuchi]

    print("Running experiments for LTL2DBA examples")
    compare_partial_algorithms(algorithms_partial,
                               tlsf_generators.ltl2dba_pg,
                               tlsf_generators.ltl2dba_pg_gen_n(),
                               preprocess=[None, None, None, None, None],
                               iterations=3,
                               step=1,
                               control_algorithm=zielonka.strong_parity_solver_no_strategies,
                               plot=True,
                               path_time="ltl2dba_partials_time.pdf",
                               path_proportion="ltl2dba_partials_proportion.pdf",
                               pkl_path="ltl2dba_data.pkl",
                               title="Comparison of partial solvers for " +
                                     "LTL2DBA parity games",
                               labels=["psol", "psolB",
                                       "psolB Buchi-safety",
                                       "psolB Buchi-coBuchi"])
    print("Running experiments for LTL2DPA examples")
    compare_partial_algorithms(algorithms_partial,
                               tlsf_generators.ltl2dpa_pg,
                               tlsf_generators.ltl2dpa_pg_gen_n(),
                               preprocess=[None, None, None, None, None],
                               iterations=3,
                               step=1,
                               control_algorithm=zielonka.strong_parity_solver_no_strategies,
                               plot=True,
                               path_time="ltl2dpa_partials_time.pdf",
                               path_proportion="ltl2dpa_partials_proportion.pdf",
                               pkl_path="ltl2dpa_data.pkl",
                               title="Comparison of partial solvers for " +
                                     "LTL2DPA parity games",
                               labels=["psol", "psolB",
                                       "psolB Buchi-safety",
                                       "psolB Buchi-coBuchi"])
    print("Running experiments for random parity games")
    compare_partial_algorithms(algorithms_partial,
                               random_games,
                               500,
                               preprocess=[None, None, None, None, None],
                               iterations=3,
                               step=2,
                               control_algorithm=zielonka.strong_parity_solver_no_strategies,
                               plot=True,
                               path_time="random_partials_time.pdf",
                               path_proportion="random_partials_proportion.pdf",
                               pkl_path="random_data.pkl",
                               title="Comparison of partial solvers for " +
                                     "random parity games",
                               labels=["psol", "psolB",
                                       "psolB Buchi-safety",
                                       "psolB Buchi-coBuchi"])


if __name__ == "__main__":
    main()
