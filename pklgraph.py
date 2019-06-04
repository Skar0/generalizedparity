import pickle
import matplotlib.pyplot as plt

f = open("all_data.pkl", "r")
(game_parameters, x, y, z) = pickle.load(f)

# game_parameters is a list of pairs (a, b)
# a is the size of the game and b is the
# number of priorities
# in (x, y, z), x is the number of nodes (yes, again)
# y contains times of solving benchmarks and
# z contains percentages of node classification

algorithms = ["psol", "psolB", "psolB Buchi-coBuchi", "psolQ"]

# we need to compute points for percentages in 5i blocks and with values from
# how many benchmarks have been classified by that much
class_pct = range(5, 105, 5)

plt.grid(True)
plt.title("Benchmark node classification")
plt.xlabel(u'classification %')
plt.ylabel(u'no. of benchmarks')

colors = ['g.', 'r.', 'b.', 'y.', 'c.']

points = []
for i in range(len(algorithms)):
    vals = []
    for p in class_pct:
        vals.append(sum([1 if v >= p else 0
                         for v in z[i]]))
    points.extend(plt.plot(class_pct, vals, colors[i], label=algorithms[i]))

plt.legend(loc='lower left', handles=points)
plt.savefig("all_pgs_classification.pdf", bbox_inches='tight')
plt.clf()
plt.close()
