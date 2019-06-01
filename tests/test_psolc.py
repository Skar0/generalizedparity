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
        print("Testing the computation of R sets from psolC")
        W, complement_W = psolC.R_set(self.jfs_example(), [(0, 4), (2, 2)])
        self.assertTrue(len(W) == 0)
        self.assertTrue(len(complement_W) == 3)


if __name__ == '__main__':
    unittest.main()
