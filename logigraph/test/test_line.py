import unittest
from logigraph.line import line

class test_line_methods(unittest.TestCase):
    def test_is_solved(self):
        testline = line(8)
        test_list = [
                 [[[], '........']    , True],
                 [[[], '_.......']    , False],
                 [[[], '._......']    , False],
                 [[[], '......._']    , False],
                 [[[2], '.xx...._']   , False],
                 [[[2], 'xx......']   , True],
                 [[[2], '...xx...']   , True],
                 [[[2], '......xx']   , True],
                 [[[2], 'x.....xx']   , False],
                 [[[2], '.x....xx']   , False],
                 [[[2], '.x...xx.']   , False],
                 [[[1,2], '.x...xx.'] , True],
                 [[[1,2], 'x.....xx'] , True],
                 [[[2,1], 'x.....xx'] , False],
                 [[[8], 'xxxxxxxx']   , True]
                ]
        for test in test_list:
            testline.index_list = test[0][0]
            testline.cells_list = list(test[0][1])
            self.assertEqual(testline.is_solved(), test[1])
