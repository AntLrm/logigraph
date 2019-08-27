from logigraph.logigraph import logigraph

if __name__ == '__main__':
    a = line(10)
    a.index_list = [1,2,2,1]
    a.cells_list = list('__________')
    print(repr(a))
    a.partial_solve()
    print(repr(a))

