from logigraph.logigraph import line

if __name__ == '__main__':
    a = line(11)
    a.index_list = [3,3,2]
    print(a.get_possible_solve_list())
