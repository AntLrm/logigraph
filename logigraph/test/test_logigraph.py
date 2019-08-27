import unittest
from logigraph.logigraph import logigraph 

class test_logigraph_methods(unittest.TestCase):
    def test_solve(self):
        testlogigraph = logigraph([[2,1],[3],[1,1],[1,1],[1]], [[1,1],[4],[1],[2],[2]])
        testlogigraph.solve()
        self.assertEqual('xx.x.', ''.join(testlogigraph.line_list[0].cells_list))
        self.assertEqual('.xxx.', ''.join(testlogigraph.line_list[1].cells_list))
        self.assertEqual('.x..x', ''.join(testlogigraph.line_list[2].cells_list))
        self.assertEqual('.x..x', ''.join(testlogigraph.line_list[3].cells_list))
        self.assertEqual('x....', ''.join(testlogigraph.line_list[4].cells_list))
