import pickle

f = open("ltl2dba_data.pkl", "r")
(x, y, z) = pickle.load(f)

algorithms = ["psol", "psolB", "psolB Buchi-safety", "psolB Buchi-coBuchi"]
print("algorithms    " + "    ".join(algorithms))
for j in range(len(z[0])):
    print("ltl2dba_" + str(j + 1) +
          "    " + "    ".join([format(z[i][j], "06.2f") for i in range(len(z))]))
