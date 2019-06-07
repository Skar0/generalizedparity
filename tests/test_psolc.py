import unittest
import file_handler
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
        W = psolC.R_set(self.jfs_example(), T, 0)
        self.assertTrue(len(W) == 2)

    def test_jfs_algo(self):
        print("Testing JFs algo on JFs example")
        expected_W = set([0, 2])
        W = psolC.jfs_algo(self.jfs_example(), 0)
        self.assertTrue(set(W) == expected_W)

    def test_jfs_algo2(self):
        print("Testing JFs algo on amba_decomposed_decode")
        g = file_handler.load_from_file(
            "examples/amba_decomposed_decode.tlsf.pg")
        expected_W = set([0, 3, 4, 5])
        W = psolC.jfs_algo(g, 0)
        self.assertTrue(set(W) == expected_W)

        expected_L = set([2, 6, 7, 8, 9])
        L = psolC.jfs_algo(g, 1)
        self.assertTrue(set(L) == expected_L)

    def test_jfs_algo3(self):
        print("Testing JFs algo on ltl2dba22")
        g = file_handler.load_from_file(
            "examples/ltl2dba22.tlsf.pg")
        # winning
        expected_W = set([])
        W = psolC.jfs_algo(g, 0)
        self.assertTrue(set(W) == expected_W)
        # losing
        expected_L = set([0, 1, 2, 3, 4, 6, 7, 8, 9, 10, 11, 13,14])
        L = psolC.jfs_algo(g, 1)
        self.assertTrue(set(L) == expected_L)

    def test_psolc(self):
        print("Testing psolc on JFs example")
        expected_W1 = set([0, 1, 2])
        _, W1, _ = psolC.psolC(self.jfs_example(), [], [])
        self.assertTrue(set(W1) == expected_W1)

    def test_psolc2(self):
        print("Testing psolc on ltl2dba_E.tlsf.pg")
        expected_W1 = set([])
        _, W1, W2 = psolC.psolC(
            file_handler.load_from_file("examples/ltl2dba_E.tlsf.pg"), [], [])
        self.assertTrue(set(W1) == expected_W1)

    def test_psolc3(self):
        print("Testing psolc algo on amba_decomposed_decode")
        g = file_handler.load_from_file(
            "examples/amba_decomposed_decode.tlsf.pg")
        expected_W1 = set([0, 3, 4, 5])
        expected_W2 = set([1, 2, 6, 7, 8, 9])
        subg, W1, W2 = psolC.psolC(g, [], [])
        self.assertTrue(set(W1) == expected_W1)
        self.assertTrue(set(W2) == expected_W2)
        self.assertTrue(len(subg.get_nodes()) == 0)

    def test_psolc4(self):
        print("Testing psolc algo on ltl2dba22")
        g = file_handler.load_from_file(
            "examples/ltl2dba22.tlsf.pg")
        expected_W1 = set([])
        expected_W2 = set(range(0, 15))
        subg, W1, W2 = psolC.psolC(g, [], [])
        self.assertTrue(set(W1) == expected_W1)
        self.assertTrue(set(W2) == expected_W2)
        self.assertTrue(len(subg.get_nodes()) == 0)


if __name__ == '__main__':
    unittest.main()
