import pickle


def timetable(game_parameters, x, y, algorithms, filename):
    f = open(filename, "w")
    f.write("benchmark name; number of vertices; number of priorities;")
    f.write(";".join(algorithms) + "\n")

    def to_string(x):
        if abs(x - 60.0) <= 2.0:
            return "T/O"
        else:
            return format(x, "09.5f").replace(".", ",")

    for j in range(len(y[0])):
        (name, n, prts) = game_parameters[j]
        f.write(name + ";")
        f.write(str(n) + ";")
        f.write(str(prts) + ";")
        f.write(";".join([to_string(y[i][j]) for i in range(len(y))]))
        f.write("\n")
    f.close()


def proportiontable(game_parameters, x, y, z, algorithms, filename):
    f = open(filename, "w")
    f.write("benchmark name; number of vertices; number of priorities;")
    f.write(";".join(algorithms) + "\n")
    for j in range(len(z[0])):
        (name, n, prts) = game_parameters[j]
        f.write(name + ";")
        f.write(str(n) + ";")
        f.write(str(prts) + ";")
        f.write(";".join([format(z[i][j], "06.2f").replace(".", ",")
                          for i in range(len(z))]))
        f.write("\n")
    f.close()


def main():
    # First, we deal with partial solvers
    algorithms = ["psolB", "psolQ", "psolC"]
    f = open("all_data.pkl", "r")
    (game_parameters, x, y, z) = pickle.load(f)
    proportiontable(game_parameters, x, z, algorithms,
                    "onedimprop-partial.csv")
    timetable(game_parameters, x, y, algorithms,
              "onedim-partial.csv")
    algorithms = ["psolB", "psolQ", "psolC"]
    f = open("allgen_data.pkl", "r")
    (game_parameters, x, y, z) = pickle.load(f)
    proportiontable(game_parameters, x, z, algorithms,
                    "genprop-partial.csv")
    timetable(game_parameters, x, y, algorithms,
              "gen-partial.csv")
    # Now we deal with complete solvers
    algorithms = ["Zielonka",
                  "Ziel + psolB",
                  "Ziel + psolQ",
                  "Ziel + psolC"]
    f = open("ziel_combo.pkl", "r")
    (game_parameters, x, y) = pickle.load(f)
    timetable(game_parameters, x, y, algorithms,
              "onedim-complete.csv")
    algorithms = ["Gen Zielonka",
                  "Gen Ziel + Gen psolB",
                  "Gen Ziel + Gen psolQ",
                  "Gen Ziel + Gen psolC"]
    f = open("genziel_combo.pkl", "r")
    (game_parameters, x, y) = pickle.load(f)
    timetable(game_parameters, x, y, algorithms,
              "gen-complete.csv")
    # Finally, we look at hard examples
    algorithms = ["psolB", "psolQ", "psolC"]
    f = open("abo_part.pkl", "r")
    (game_parameters, x, y, z) = pickle.load(f)
    proportiontable(game_parameters, x, z, algorithms,
                    "aboprop-partial.csv")
    timetable(game_parameters, x, y, algorithms,
              "abo-partial.csv")
    algorithms = ["Zielonka",
                  "Ziel + psolB",
                  "Ziel + psolQ",
                  "Ziel + psolC"]
    f = open("abo_ziel.pkl", "r")
    (game_parameters, x, y) = pickle.load(f)
    timetable(game_parameters, x, y, algorithms,
              "abo-complete.csv")


if __name__ == "__main__":
    main()
