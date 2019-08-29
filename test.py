from logigraph.logigraph import logigraph
from logigraph.solver import linear_solver, edge_logic_solver, absurd_solver

log = logigraph()
log.set_from_file('logigraph_inputs/absurd.txt')
l = linear_solver()
e = edge_logic_solver()
a = absurd_solver()

e.solve(log)
l.solve(log)
a.solve(log)


print(log)
print(log.is_lineary_solvable)
print(log.is_possible)
print(log.is_solved())
