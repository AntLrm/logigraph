import unittest
import random
from logigraph.logigraph import line

class test_line_methods(unittest.TestCase):
    def test_is_offset_ok(self):
        testline = line(5)
        
        index_list_list = [
                [3],
                [3,1]
                ]
        for index_list in index_list_list:
            testline.index_list = index_list
            expected_dict = {
                    '_____': {0: True, 1: True, 2: True, 3: False, 4: False, 5: False},
                    '____.': {0: True, 1: True, 2: False, 3: False, 4: False, 5: False},
                    '___._': {0: True, 1: False, 2: False, 3: False, 4: False, 5: False},
                    '__.__': {0: False, 1: False, 2: False, 3: False, 4: False, 5: False},
                    '_.___': {0: False, 1: False, 2: True, 3: False, 4: False, 5: False},
                    '.____': {0: False, 1: True, 2: True, 3: False, 4: False, 5: False},
                    'x.___': {0: False, 1: False, 2: True, 3: False, 4: False, 5: False},
                    'x.x__': {0: False, 1: False, 2: True, 3: False, 4: False, 5: False},
                    '__x._': {0: True, 1: False, 2: False, 3: False, 4: False, 5: False},
                    '____x': {0: True, 1: False, 2: True, 3: False, 4: False, 5: False}
                    }
            for line_cells_string in expected_dict.keys():
                testline.cells_list = list(line_cells_string)
                input_expected_dict = expected_dict[line_cells_string]
                for offset in input_expected_dict.keys():
                    self.assertEqual(input_expected_dict[offset], testline.is_offset_ok(offset))

    def test_get_remaining_line(self):
        testline = line(20)
        testline.index_list = [2,3,1]
        for cell_nbr in range(20):
            testline.cells_list[cell_nbr] = random.choice(['_', '.', 'x'])
       
        for offset in [0, 20, 21, random.randint(1,20)]:
            remaining_line = testline.get_remaining_line(offset)
            self.assertEqual(testline.index_list[1:], remaining_line.index_list)
            start = offset + 3
            self.assertEqual(testline.cells_list[start:], remaining_line.cells_list)

    def test_merge_lines(self):
        testline = line(10)
        testline.index_list=[3]
        testlinecells_dict= {
                '__________': {'xxxx': '..xxx.xxxx', '_.x': '...xxx._.x', 'xxxxxx': 'xxx.xxxxxx', 'xxxxxxxxx': '__________'},
                '__.___._x_': {'xxxx': '__________', 'xxx': '...xxx.xxx', 'xxx.xxx': '__________'},
                '_____xxx.x': {'xxxx': '__________', 'xxxx.x': 'xxx.xxxx.x'},
                '___.x_x_.x': {'x_xx.x' : 'xxx.x_xx.x'}
                }
        for testlinecells in testlinecells_dict.keys():
            testline.cells_list = list(testlinecells)
            expected_dict = testlinecells_dict[testlinecells]
            for endline_cells in expected_dict.keys():
                endline = line(len(endline_cells))
                endline.cells_list = list(endline_cells)
                self.assertEqual(expected_dict[endline_cells], ''.join(testline.merge_lines(endline).cells_list))
                
    def test_get_common_line(self):
        testline =line(10)
        lines_to_compare = []
        cells_to_compare = [
                '__.x._xx..',
                '__.x.xxx..',
                '__.x.xxx..',
                '__.x.xxx..',
                '__.x.xxx..',
                '__.x.xxx._',
                '__.x.xx_..',
                '__.x.xx_..',
                '__.x.xxx..',
                '__.x_xxx..'
                ]

        for cells_str in cells_to_compare:
            line_to_add = line(10)
            line_to_add.cells_list = list(cells_str)
            lines_to_compare.append(line_to_add)

        self.assertEqual('__.x__x_._', ''.join(testline.get_common_line(lines_to_compare).cells_list))
       
