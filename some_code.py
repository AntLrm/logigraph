from logigraph.logigraph import logigraph
from logigraph.solver import linear_solver, edge_logic_solver, absurd_solver

log = logigraph()
log.set_from_file('logigraph_inputs/nolinear.txt')
l = linear_solver()
e = edge_logic_solver()
a = absurd_solver()

l.solve(log)
print(log)
log.set_from_file('logigraph_inputs/nolinear.txt')
a.solve(log)
print(log)
print(log.is_possible)
