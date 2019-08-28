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
