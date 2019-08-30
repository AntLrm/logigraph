import random
import unittest
from logigraph.solver import linear_solver, absurd_solver, edge_logic_solver
from logigraph.logigraph import logigraph

class test_line_solver_methods(unittest.TestCase):
    def impossible_solve_try(self):
        test_logigraph = logigraph([[2],[1,1],[1],[1],[1],[2]],[[1,1],[1],[1],[2],[2]])
        linear = linear_solver()
        absurd = absurd_solver()

        linear.solve(test_logigraph)
        assertEqual(test_logigraph.is_solved(), False)
        assertEqual(test_logigraph.is_lineary_solvable(), False)

        absurd.solve(test_logigraph)
        assertEqual(test_logigraph.is_solved(), False)
        assertEqual(test_logigraph.is_lineary_solvable, False)
        assertEqual(test_logigraph.is_possible, False)

    def absurd_solve_try(self):
        test_logigraph = logigraph([[2],[1,1],[1],[1],[2]],[[1,1],[1],[1],[2],[2]])
        linear = linear_solver()
        edge = edge_solver()
        absurd = absurd_solver()

        linear.solve(test_logigraph)
        assertEqual(test_logigraph.is_solved(), False)
        assertEqual(test_logigraph.is_lineary_solvable(), False)
        string_repr = '\n     1, , , , ,\n     1,1,1,2,2,\n   2|_|_|_|_|_|\n 1,1|_|_|_|_|_|\n   1|_|_|_|_|_|\n   1|_|_|_|_|_|\n   2|_|_|_|_|_|'
        assertEqual(string_repr, repr(test_logigraph))

        edge.solve(test_logigraph)
        assertEqual(test_logigraph.is_solved(), False)
        assertEqual(test_logigraph.is_lineary_solvable(), False)
        assertEqual(test_logigraph.is_possible, True)
        string_repr = '\n     1, , , , ,\n     1,1,1,2,2,\n   2|_|_|_|_|.|\n 1,1|_|_|_|_|_|\n   1|_|_|_|_|_|\n   1|_|_|_|_|_|\n   2|_|_|_|_|.|'
        assertEqual(string_repr, repr(test_logigraph))

        linear.solve(test_logigraph)
        assertEqual(test_logigraph.is_solved(), False)
        assertEqual(test_logigraph.is_possible, True)
        assertEqual(test_logigraph.is_lineary_solvable(), False)
        string_repr = '\n     1, , , , ,\n     1,1,1,2,2,\n   2|_|_|_|_|.|\n 1,1|_|_|_|_|_|\n   1|.|.|.|.|x|\n   1|_|_|_|_|_|\n   2|_|_|_|_|.|'
        assertEqual(string_repr, repr(test_logigraph))

        absurd.solve(test_logigraph)
        assertEqual(test_logigraph.is_solved(), True)
        assertEqual(test_logigraph.is_possible, True)
        string_repr = '\n     1, , , , ,\n     1,1,1,2,2,\n   2|.|.|x|x|.|\n 1,1|x|.|.|x|.|\n   1|.|.|.|.|x|\n   1|.|.|.|.|x|\n   2|x|x|.|.|.|'
        assertEqual(string_repr, repr(test_logigraph))

        test_logigraph = logigraph([[2],[1,1],[1],[1],[2]],[[1,1],[1],[1],[2],[2]])
        absurd.solve(test_logigraph)
        assertEqual(test_logigraph.is_solved(), True)
        assertEqual(test_logigraph.is_possible, True)
        string_repr = '\n     1, , , , ,\n     1,1,1,2,2,\n   2|.|.|x|x|.|\n 1,1|x|.|.|x|.|\n   1|.|.|.|.|x|\n   1|.|.|.|.|x|\n   2|x|x|.|.|.|'
        assertEqual(string_repr, repr(test_logigraph))

    def random_solve_try(self):
        test_logigraph = logigraph()
        col_size = random.randint(4,12)
        line_size = random.randint(4,12)
        
        for line_nbr in range(col_size):
            rand_line_pattern = []
            for cell_nbr in range(line_size):
                cell = random.choice(['.', 'x'])
                rand_line_pattern.append(cell) 

            test_line = line(line_size)
            test_line.cells_list = rand_line_pattern
            test_line.index_list = test_line.get_index_from_pattern()

            test_logigraph.line_list.append(test_line)
        test_logigraph.transpose()
        for col_nbr in range(line_size):
            test_logigraph.line_list[col_nbr].index_list = line_list[col_nbr].get_index_from_pattern()

        test_logigraph.transpose()
        
        for line_nbr in range(col_size):
            test_logigraph.line_list[line_nbr].cells_list = line_size * ['_']

        linear = linear_solver()
        linear.solve(test_logigraph)
        if test_logigraph.is_full():
            self.assertEqual(True, test_logigraph.is_solved())
            self.assertEqual(True, test_logigraph.is_lineary_solvable)
            self.assertEqual(True, test_logigraph.is_possible)
        
        for line_nbr in range(col_size):
            test_logigraph.line_list[line_nbr].cells_list = line_size * ['_']

        absurd = absurd_solver()
        absurd.solve(test_logigraph)
        self.assertEqual(True, test_logigraph.is_full())
        self.assertEqual(True, test_logigraph.is_solved())
        self.assertEqual(True, test_logigraph.is_lineary_solvable)
        self.assertEqual(True, test_logigraph.is_possible)
