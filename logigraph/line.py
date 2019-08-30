from copy import deepcopy

class line():
    def __init__(self, lenght):
        self.cells_list = lenght * ['_']
        self.index_list = []
        self.size = lenght
        self.has_been_updated = True
        
    def __repr__(self):
        index_string = self.repr_index()
        cells_string = ''.join(self.cells_list)
        return index_string + cells_string     

    def repr_index(self, offset = 0):
        if offset != 0:
            prefix_space = ''.join((offset - len(self.repr_index()))*[' '])
        else:
            prefix_space = ''

        return prefix_space + ','.join([str(index) for index in self.index_list]) + '|'

    #TODO test on this method
    def is_solved(self):
        if '_' in self.cells_list :
            return False
        else:
            block_list = self.get_index_from_pattern()
            if block_list == self.index_list:
                return True
            else:
                return False

    def get_index_from_pattern(self):
        if '_' in self.cells_list :
            return []
        else:
            block_list = []
            new_block = True
            for cell_nbr, cell in enumerate(self.cells_list):
                if cell == 'x':
                    if new_block :
                        block_size = 1
                        new_block = False
                    else :
                        block_size += 1
                elif cell == '.':
                    if not new_block :
                        block_list.append(block_size)
                        block_size = 0
                        new_block = True
            if not new_block :
                block_list.append(block_size)
        return block_list
