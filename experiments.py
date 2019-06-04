#!/usr/bin/env python


import os
import fnmatch
import zielonka
import generators
import fatalattractors.psol as psol
import fatalattractors.psolB as psolB
import fatalattractors.psolC as psolC
import fatalattractors.psolQ as psolQ
#import fatalattractors.psol_generalized as psol_generalized
#import fatalattractors.psolB_generalized as psolB_generalized
import file_handler
from benchmarks.compare_algorithms import compare_partial_algorithms


def random_games(i):
    # for some reason this does not work for indices < 5
    j = i + 5
    return generators.random(j, j, 1, j / 3)


def main():

    labels = ["psol", "psolB", "psolB Buchi-coBuchi", "psolQ", "psolC"]
    algorithms_partial = [psol.psol,
                          psolB.psolB,
                          psolB.psolB_buchi_cobuchi,
                          psolQ.psolQ,
                          psolC.psolC]

    print("Running experiments for all files in ./examples")
    sample_files = filter(lambda f: fnmatch.fnmatch(f, "*.pg"),
                          os.listdir("./examples"))
    num_examples = len(sample_files)

    def all_examples(i):
        return file_handler.load_from_file(
            os.path.join("examples", sample_files[i]))
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
                               control_algorithm=zielonka.strong_parity_solver_no_strategies,
                               pkl_path="all_data.pkl")
    # generalized parity games now
    algorithms_general = [psol_generalized.psol,
                          psolB_generalized.psolB]

    # print("experiments for generalized parity games: all files in ./examples")
    # sample_files = filter(lambda f: fnmatch.fnmatch(f, "*.gpg"),
    #                       os.listdir("./examples"))
    # num_examples = len(sample_files)

    # def all_examples(i):
    #     return file_handler.load_from_file(
    #         os.path.join("examples", sample_files[i]))
    # compare_partial_algorithms(algorithms_general,
    #                            all_examples,
    #                            num_examples,
    #                            preprocess=[None, None, None, None, None],
    #                            iterations=3,
    #                            step=1,
    #                            plot=True,
    #                            path_time="allgen_time.pdf",
    #                            path_proportion="allgen_prop.pdf",
    #                            path_bulkprop="allgen_bulkprop.pdf",
    #                            control_algorithm=zielonka.strong_parity_solver_no_strategies,
    #                            pkl_path="allgen_data.pkl")


if __name__ == "__main__":
    main()
