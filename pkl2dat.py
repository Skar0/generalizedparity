import pickle

f = open("all_data.pkl", "r")
(game_parameters, x, y, z) = pickle.load(f)

algorithms = ["psol", "psolB", "psolB Buchi-coBuchi", "psolQ"]
print("algorithms    " + "    ".join(algorithms))
for j in range(len(z[0])):
    (n, prts) = game_parameters[j]
    print("benchmark " + str(j + 1) +
          "(n=" + str(n) + ",prts=" + str(prts) + ")"
          "    " + "    ".join([format(z[i][j], "06.2f") for i in range(len(z))]))
