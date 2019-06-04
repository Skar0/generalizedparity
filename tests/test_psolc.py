import unittest
from graph import Graph
from fatalattractors import psolC


class TestPSolC(unittest.TestCase):
    def jfs_example(self):
        g = Graph()
        g.add_node(0, (0, 4))
        g.add_node(1, (0, 3))
        g.add_node(2, (0, 2))
        g.add_edge(0, 0)
        g.add_edge(0, 1)
        g.add_edge(1, 2)
        g.add_edge(2, 2)
        g.add_edge(2, 3)
        return g

    def test_R(self):
        print("Testing the computation of R sets from psolC - on JFs example")
        T = [(0, 2), (0, 4), (1, 2), (1, 4), (2, 2), (2, 4)]
        W, complement_W = psolC.R_set(self.jfs_example(), T)
        print(W)
        self.assertTrue(len(W) == 2)
        self.assertTrue(len(complement_W) == 1)


    def test_jfs_algo(self):
        print("Testing JFs algo on JFs example")
        expected_W = set([0, 2])
        W = psolC.jfs_algo(self.jfs_example())
        self.assertTrue(set(W) == expected_W)


    def test_psolc(self):
        print("Testing psolc on JFs example")
        expected_W1 = set([0, 1, 2])
        _, W1, _ = psolC.psolC(self.jfs_example(), [], [])
        self.assertTrue(set(W1) == expected_W1)


if __name__ == '__main__':
    unittest.main()
