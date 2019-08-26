import pdb

class line():
    def __init__(self, lenght):
        self.cells_list = lenght * ['_']
        self.index_list = []
        self.size = lenght
        
    def __repr__(self):
        index_str_list = []
        for index in self.index_list:
            index_str_list.append(str(index))
        index_string = ''.join(index_str_list)
        cells_string = ''.join(self.cells_list)
        return index_string + '|' + cells_string     

    def partial_solve(self):
        partial_solution = self.get_common_line(self.get_possible_solve_list())
        self.cells_list = partial_solution.cells_list[:]

    def get_possible_solve_list(self):
        possible_solve_list = []
        if self.index_list == []:
            if 'x' in self.cells_list:
                return []
            else:
                emptyline = line(self.size)
                emptyline.cells_list = self.size * ['.']
                return [emptyline] 

        for offset in range(self.size):
            if self.is_offset_ok(offset):
                remaining_line = self.get_remaining_line(offset)
                remaining_line_possible_solve_list = remaining_line.get_possible_solve_list()
                if len(remaining_line_possible_solve_list) > 0:
                    for remaining_line_possible_solve in remaining_line_possible_solve_list:
                        possible_solve_list.append(self.merge_lines(remaining_line_possible_solve))
                        
        return possible_solve_list

    def get_common_line(self, lines_to_compare):
        common_line = line(self.size)
        common_line.index_list = self.index_list
        for cell_nbr in range(self.size):
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


    def is_offset_ok(self, offset):                             
        if offset > self.size:
            return False
        
        first_index = self.index_list[0]
        for block_cell in range(first_index):
            if offset + block_cell >= self.size:
                return False
            if self.cells_list[offset + block_cell] == '.':
                return False

        if offset + first_index < self.size:
            if self.cells_list[offset + first_index] == 'x':
                return False
        if offset != 0:
            if self.cells_list[offset - 1] == 'x':
                return False
        return True


    def get_remaining_line(self, offset):
        first_index = self.index_list[0]
        starting_cell = offset + first_index + 1
        remaining_line = line(self.size - starting_cell)
        remaining_line.index_list = self.index_list[1:]
        remaining_line.cells_list = self.cells_list[starting_cell:]
        return remaining_line


    def merge_lines(self, endline):
        merged_line = line(self.size)
        merged_line.cells_list = self.cells_list[:]
        merged_line.index_list = self.index_list
        offset = self.size - endline.size - self.index_list[0] - 1
        
        if offset < 0:
            print('Error during merging, out of range')
            return line(self.size)

        'writing first block'
        if offset != 0 :
            for cell_number in range(offset):
                merged_line.cells_list[cell_number] = '.'
        for cell_number in range(offset, offset + self.index_list[0]):
            merged_line.cells_list[cell_number] = 'x'
        if offset + self.index_list[0] < merged_line.size:
            merged_line.cells_list[offset+self.index_list[0]] = '.'
        
        'writing remaining block with position'
        for cell_number in range(endline.size): 
            original_cell = self.cells_list[cell_number + self.size - endline.size]
            endline_cell = endline.cells_list[cell_number]

            if original_cell == '_':
                merged_line.cells_list[cell_number + self.size - endline.size] = endline_cell
            elif original_cell != endline_cell:
                pdb.set_trace()
                print('Error during merging, a conflict happened')
                return line(self.size)
                
        return merged_line

