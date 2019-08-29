import unittest
from logigraph.logigraph import logigraph 
from logigraph.solver import edge_logic_solver

class test_logigraph_methods(unittest.TestCase):
    def test_solve(self):
        testlogigraph = logigraph([[2],[1,1],[1],[1],[1],[2]],[[1,1],[1],[1],[2],[2]])
        testsolver = edge_logic_solver()
        testsolver.solve(testlogigraph)
        self.assertEqual('____.', ''.join(testlogigraph.line_list[0].cells_list))
        self.assertEqual('_____', ''.join(testlogigraph.line_list[1].cells_list))
        self.assertEqual('_____', ''.join(testlogigraph.line_list[2].cells_list))
        self.assertEqual('_____', ''.join(testlogigraph.line_list[3].cells_list))
        self.assertEqual('_____', ''.join(testlogigraph.line_list[4].cells_list))
        self.assertEqual('____.', ''.join(testlogigraph.line_list[5].cells_list))
