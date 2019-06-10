#!/usr/bin/env python


import sys
import os
import fnmatch
import zielonka
import generalized_parity_recursive as gpg
import generalized_zielonka_with_partials as genpartial
import generators
import fatalattractors.psolB as psolB
import fatalattractors.psolC as psolC
import fatalattractors.psolQ as psolQ
import fatalattractors.psol_generalized as psol_generalized
import fatalattractors.psolB_generalized as psolB_generalized
import fatalattractors.psolQ_generalized as psolQ_generalized
import file_handler
from benchmarks.compare_algorithms import compare_partial_algorithms, compare_complete_algorithms_LTLbenchmarks


def random_games(i):
    # for some reason this does not work for indices < 5
    j = i + 5
    return generators.random(j, j, 1, j / 3)


sample_files = filter(lambda f: fnmatch.fnmatch(f, "*.pg"),
                      os.listdir("./examples"))
num_examples = len(sample_files)


def all_examples(i):
    print(sample_files[i])
    return file_handler.load_from_file(
        os.path.join("examples", sample_files[i]))


gen_sample_files = filter(lambda f: fnmatch.fnmatch(f, "*.gpg"),
                          os.listdir("./examples"))
num_gen_examples = len(gen_sample_files)


def all_generalized_examples(i):
    return file_handler.load_generalized_from_file(
        os.path.join("examples", gen_sample_files[i]))


def complete():
    # Zielonka + partial solvers now
    algorithms_partial_zielonka = [zielonka.strong_parity_solver_no_strategies,
                                   zielonka.zielonka_with_psol,
                                   zielonka.zielonka_with_psolB,
                                   zielonka.zielonka_with_psolB_buchi_safety,
                                   zielonka.zielonka_with_single_psolB_iteration,
                                   zielonka.zielonka_with_psolQ,
                                   zielonka.zielonka_with_psolC]

    labels_partial_zielonka = ["Zielonka",
                               "Ziel + psol",
                               "Ziel + psolB",
                               "Ziel + psolB buchi-safety",
                               "Ziel + one psolB step ",
                               "Ziel + psolQ",
                               "Ziel + psolC"]

    compare_complete_algorithms_LTLbenchmarks(
        algorithms_partial_zielonka,
        all_examples,
        num_examples,
        preprocess=[None] * len(labels_partial_zielonka),
        iterations=3,
        step=1,
        check_solution=False,
        plot=True,
        path="all_ziel.pdf",
        path_tot="all_ziel_cumulative.pdf",
        title="Comparison of Zielonka + partial solver on LTL benchmarks",
        labels=labels_partial_zielonka)

    algorithms_partial_genzielonka = [gpg.generalized_parity_solver,
                                      genpartial.generalized_zielonka_with_psol,
                                      genpartial.generalized_with_psolB,
                                      genpartial.generalized_zielonka_with_psolQ]

    labels_partial_genzielonka = ["Gen Zielonka",
                                  "Gen Ziel + Gen psol",
                                  "Gen Ziel + Gen psolB",
                                  "Gen Ziel + Gen psolQ"]

    compare_complete_algorithms_LTLbenchmarks(
        algorithms_partial_genzielonka,
        all_generalized_examples,
        num_gen_examples,
        preprocess=[None] * len(labels_partial_genzielonka),
        iterations=3,
        step=1,
        check_solution=False,
        plot=True,
        path="genziel+partials-time.pdf",
        path_tot="genziel+partials-cumulative.pdf",
        title="Comparison of Gen Zielonka + partial solver on LTL benchmarks",
        labels=labels_partial_genzielonka)


def partial():
    labels = ["psolB", "psolB Buchi-coBuchi", "psolQ", "psolC"]
    algorithms_partial = [psolB.psolB,
                          psolB.psolB_buchi_cobuchi,
                          psolQ.psolQ,
                          psolC.psolC]

    print("Running experiments for all files in ./examples")

    compare_partial_algorithms(algorithms_partial,
                               all_examples,
                               num_examples,
                               preprocess=[None, None, None, None, None],
                               iterations=3,
                               step=1,
                               labels=labels,
                               plot=True,
                               path_time="all_time.pdf",
                               path_proportion="all_prop.pdf",
                               path_bulkprop="all_bulkprop.pdf",
                               path_tottime="all_tottime.pdf",
                               control_algorithm=zielonka.strong_parity_solver_no_strategies,
                               pkl_path="all_data.pkl")

    # generalized parity games now
    labels = ["psol", "psolB", "psolQ", "psolC"]
    algorithms_general = [psol_generalized.psol_generalized,
                          psolB_generalized.psolB_generalized_inline,
                          psolQ_generalized.psolQ_generalized]

    print("experiments for generalized parity games: all files in ./examples")

    compare_partial_algorithms(algorithms_general,
                               all_generalized_examples,
                               num_gen_examples,
                               preprocess=[None, None, None, None, None],
                               iterations=3,
                               step=1,
                               labels=labels,
                               plot=True,
                               path_time="allgen_time.pdf",
                               path_proportion="allgen_prop.pdf",
                               path_bulkprop="allgen_bulkprop.pdf",
                               path_tottime="allgen_tottime.pdf",
                               control_algorithm=gpg.generalized_parity_solver,
                               pkl_path="allgen_data.pkl")


if __name__ == "__main__":
    assert(len(sys.argv) == 2)
    if sys.argv[1] == "complete":
        complete()
    elif sys.argv[1] == "partial":
        partial()
    else:
        assert(False)
