from copy import deepcopy
from logigraph.line import line

class linear_solver():
    def __init__(self):
        self.max_loop = 500

    #TODO instead of checking for max loop, check if no lines nor column have been updated during 1 cycles.
    def solve(self, logigraph):
        print('running...')
        loop = 0
        while logigraph.is_not_solved() and loop < self.max_loop:
            loop += 1
            logigraph.col_state_list = [False]* len(logigraph.col_state_list)
            for line in logigraph.line_list:
                if line.has_been_updated:
                    partial_solve = self.line_partial_solve(line)
                    for cell_nbr, cell in enumerate(partial_solve.cells_list):
                        if cell != line.cells_list[cell_nbr]:
                            logigraph.col_state_list[cell_nbr] = True
                    line.cells_list = deepcopy(partial_solve.cells_list)
            logigraph.transpose()

        if logigraph.is_transposed:
            logigraph.transpose()
        
        if loop == self.max_loop:
            print('max number of iteration reached')
        else: 
            print('done')

    def line_partial_solve(self, mline):
        return self.get_common_line(self.get_possible_solve_list(mline))

    def get_possible_solve_list(self, mline):
        possible_solve_list = []

        if mline.index_list == [] or mline.index_list == [0]:
            if 'x' in mline.cells_list:
                return []
            else:
                emptyline = line(mline.size)
                emptyline.cells_list = mline.size * ['.']
                return [emptyline] 

        for offset in range(mline.size):
            if self.is_offset_ok(mline, offset):
                remaining_line = self.get_remaining_line(mline, offset)
                remaining_line_possible_solve_list = self.get_possible_solve_list(remaining_line)
                if len(remaining_line_possible_solve_list) > 0:
                    for remaining_line_possible_solve in remaining_line_possible_solve_list:
                        possible_solve_list.append(self.merge_lines(mline, remaining_line_possible_solve))
                        
        return possible_solve_list

    def get_common_line(self, lines_to_compare):
        common_line = line(lines_to_compare[0].size)
        common_line.index_list = lines_to_compare[0].index_list
        for cell_nbr in range(lines_to_compare[0].size):
            if self.check_equal([item.cells_list[cell_nbr] for item in lines_to_compare]):
                common_line.cells_list[cell_nbr] = lines_to_compare[0].cells_list[cell_nbr]
        return common_line

    def check_equal(self, iterator):
        iterator = iter(iterator)
        try:
            first = next(iterator)
        except StopIteration:
            return True
        return all(first == rest for rest in iterator)


    def is_offset_ok(self, mline, offset):                             
        first_index = mline.index_list[0]
        for block_cell in range(first_index):
            if offset + block_cell >= mline.size:
                return False
            if mline.cells_list[offset + block_cell] == '.':
                return False

        if offset + first_index < mline.size:
            if mline.cells_list[offset + first_index] == 'x':
                return False
        if 'x' in mline.cells_list[:offset]:
            return False
        return True


    def get_remaining_line(self, mline, offset):
        first_index = mline.index_list[0]
        starting_cell = offset + first_index + 1
        remaining_line = line(mline.size - starting_cell)
        remaining_line.index_list = mline.index_list[1:]
        remaining_line.cells_list = mline.cells_list[starting_cell:]
        return remaining_line


    def merge_lines(self, mline, endline):
        merged_line = line(mline.size)
        merged_line.cells_list = deepcopy(mline.cells_list)
        merged_line.index_list = deepcopy(mline.index_list)
        offset = mline.size - endline.size - mline.index_list[0] - 1
        
        if offset < 0:
            print('Error during merging, out of range')
            return line(mline.size)

        'writing first block'
        if offset != 0 :
            for cell_number in range(offset):
                merged_line.cells_list[cell_number] = '.'
        for cell_number in range(offset, offset + mline.index_list[0]):
            merged_line.cells_list[cell_number] = 'x'
        if offset + mline.index_list[0] < merged_line.size:
            merged_line.cells_list[offset+mline.index_list[0]] = '.'
        
        'writing remaining block with position'
        for cell_number in range(endline.size): 
            original_cell = mline.cells_list[cell_number + mline.size - endline.size]
            endline_cell = endline.cells_list[cell_number]

            if original_cell == '_':
                merged_line.cells_list[cell_number + mline.size - endline.size] = endline_cell
            elif original_cell != endline_cell:
                print('Error during merging, a conflict happened')
                return line(mline.size)
                
        return merged_line

class edge_logic_solver():
    def __init__(self):
        self.cases_dict = {
                'top' : [0,1],
                'bottom' : [-1,-2],
                'left' : [0,1],
                'right' : [-1,-2]
                }                
        
    def solve(self, logigraph):
        l_solver = linear_solver()
        for case in self.cases_dict:
            self.set_lines_and_index(logigraph, case)
            edge_linear_solve_list = l_solver.get_possible_solve_list(self.edge_line)
            edge_solve_list = []
            for possible_solution in edge_linear_solve_list:
                pattern_on_adjacent_line = self.get_pattern_on_adjacent_line(possible_solution)
                if self.is_pattern_ok(pattern_on_adjacent_line):
                    edge_solve_list.append(possible_solution)
            partial_solve = l_solver.get_common_line(edge_solve_list)
            self.set_logigraph_line(logigraph, partial_solve, case)

    def set_lines_and_index(self, logigraph, case):
        if case in ['left', 'right']:
            logigraph.transpose()

        self.edge_line = logigraph.line_list[self.cases_dict[case][0]]
        self.adjacent_line = logigraph.line_list[self.cases_dict[case][1]]
        self.trans_index_list = [logigraph.col_index_list[col][self.cases_dict[case][0]] for col in range(logigraph.col_nbr)]

        if logigraph.is_transposed:
            logigraph.transpose()

    def get_pattern_on_adjacent_line(self, possible_solution):
        pattern_on_adjacent_line = deepcopy(self.adjacent_line)
        for cell_nbr, cell in enumerate(possible_solution.cells_list):
            if cell == 'x':
                if self.trans_index_list[cell_nbr] > 1 :
                    pattern_on_adjacent_line.cells_list[cell_nbr] = 'x'
        return pattern_on_adjacent_line
                    
    def is_pattern_ok(self, pattern):
        l_solver = linear_solver()
        if len(l_solver.get_possible_solve_list(pattern)) > 0:
            return True
        else :
            return False

    def set_logigraph_line(self, logigraph, line, case):
        if case in ['left', 'right']:
            logigraph.transpose()

        logigraph.line_list[self.cases_dict[case][0]] = line
        
        if logigraph.is_transposed:
            logigraph.transpose()
