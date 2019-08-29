import pdb
from numpy import transpose, array
from logigraph.line import line

class logigraph():
    def __init__(self, line_index_list = [[]] , col_index_list= [[]]):
        self.line_list = []
        self.col_index_list = []
        self.is_transposed = False
        self.line_nbr = len(line_index_list)
        self.col_nbr = len(col_index_list)
        self.col_state_list = [True] * len(col_index_list)

        for col in range(self.col_nbr):
            self.add_col_index(col_index_list[col], col)
        for line in range(self.line_nbr):
            self.add_empty_line(line_index_list[line], len(col_index_list))

    #TODO: clean names and overall in __repr__ and col_index_string
    def __repr__(self):
        if self.line_nbr == 0 or self.col_nbr == 0 :
            return "Empty logigraph"

        offset_line = 1 + max(len(line.repr_index()) for line in self.line_list) 
        offset_col = max([len(index) for index in self.col_index_list])
        col_index_string_list = self.get_col_index_string_list(offset_col)
        col_string = self.col_index_string(col_index_string_list, offset_line, offset_col)
        line_string = ''

        for line in self.line_list:
            line_string = line_string + '\n' + line.repr_index(offset_line) + self.repr_canvas_line(line, col_index_string_list)
        return col_string + line_string

    def get_col_index_string_list(self, offset_col):
        col_index_string_list = []

        for col_index in self.col_index_list: 
            col_string = (offset_col - len(col_index))*[' ']
            col_string.extend([str(index) for index in col_index])
            col_index_string_list.append(col_string)
            col_index_string_list.append(offset_col * [','])

        for col_index_string in col_index_string_list:
           col_size = max([len(str(index)) for index in col_index_string]) 
           if col_size > 1:
               for i in range(len(col_index_string)):
                   col_index_string[i] = ' ' * (col_size - len(col_index_string[i])) + col_index_string[i]
        
        return col_index_string_list

    def col_index_string(self, col_index_string_list, offset_line, offset_col):
        
        offseted_col_index_string_list = [] 
        for i in range(offset_line):
            offseted_col_index_string_list.append(offset_col * [' '])
        offseted_col_index_string_list.extend(col_index_string_list)
        col_array = array(offseted_col_index_string_list).transpose()

        string_repr = ''
        for string_line in col_array:
            string_repr = string_repr + '\n' + ''.join(string_line)
        return string_repr

    def repr_canvas_line(self, line, col_index_string_list):
        canvas_line_string = ''
        col = 0
        for col_index_string in col_index_string_list:
            if col_index_string[0] == ',':
                col += 1
            else:
                col_size = max([len(str(index)) for index in col_index_string]) 
                canvas_line_string = canvas_line_string + (col_size - 1) * ' ' + line.cells_list[col] + '|'
        return canvas_line_string
        
    #TODO clean this monstruosity of a method + add try catch on int() cast
    def set_from_file(self, filepath):
        try:
            file_reader = open(filepath, 'r')
        except IOError :
            print('error while opening input file, check existence')

        col_index_list = []
        line_index_list = []
        canvas_line = 0
        index_string = ''
        line_read = 0
        for line in file_reader:
            if '|' not in line:
                col = 0
                for car in line:
                    if car != ',':
                        if car in '0123456789' :
                            index_string = index_string + car

                    elif index_string == '':
                        if line_read == 0:
                            col_index_list.append([])
                        col +=1

                    else:
                        if line_read == 0: 
                            col_index_list.append([])
                        col_index_list[col].append(int(index_string))
                        index_string = ''
                        col +=1
            else:
                line_index_list.append([])
                for car in line:
                    if car == '|':
                        if index_string != '':
                            line_index_list[canvas_line].append(int(index_string))
                            index_string = ''
                        else:
                            break
                    else:
                        if car != ',':
                            if car in '0123456789':
                                index_string = index_string + car    
                        else:
                            line_index_list[canvas_line].append(int(index_string))
                            index_string = ''
                canvas_line += 1        
            line_read += 1
        self.__init__(line_index_list, col_index_list)

    def add_empty_line(self, index_list, size):
        line_to_add = line(size)
        line_to_add.index_list = index_list
        self.line_list.append(line_to_add)

    def add_col_index(self, col_index_list, col_nbr):
        self.col_index_list.append(col_index_list)

    def is_not_solved(self):
        return any('_' in line.cells_list for line in self.line_list)

    def transpose(self):
        is_transposed = not self.is_transposed
        canvas_array = self.get_canvas_array() 
        transposed_canvas_array = canvas_array.transpose()
        col_state_list = self.col_state_list
        self.__init__(self.col_index_list, [item.index_list for item in self.line_list])
        self.set_canvas(transposed_canvas_array)
        self.is_transposed = is_transposed
        for line_nbr, line in enumerate(self.line_list):
            line.has_been_updated = col_state_list[line_nbr]

    def get_canvas_array(self):
        return array([line.cells_list for line in self.line_list])

    def set_canvas(self, canvas):
        line_index = 0
        for line in self.line_list:
            line.cells_list = canvas[line_index]
            line_index +=1 
