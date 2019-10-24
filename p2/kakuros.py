from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

from ortools.sat.python import cp_model

model = cp_model.CpModel()
solver = cp_model.CpSolver()


x1 = model.NewIntVar(0, 9, "x1")
x2 = model.NewIntVar(0, 9, "x2")
x3 = model.NewIntVar(0, 9, "x3")

xList = [x1, x2, x3]

model.AddAllDifferent(xList)

y1 = model.NewIntVar(0, 9, "y1")
y2 = model.NewIntVar(0, 9, "y2")
y3 = model.NewIntVar(0, 9, "y3")

yList = [y1, y2, y3]

model.AddAllDifferent(yList)

z1 = model.NewIntVar(0, 9, "z1")
z2 = model.NewIntVar(0, 9, "z2")
z3 = model.NewIntVar(0, 9, "z3")

zList = [z1, z2, z3]

model.AddAllDifferent(zList)

firstColumn = [x1, y1, z1]
secondColumn = [x2, y2, z2]
thirdColumn = [x3, y3, z3]

model.AddAllDifferent(firstColumn)
model.AddAllDifferent(secondColumn)
model.AddAllDifferent(thirdColumn)

model.Add(x1 + x2 + x3 == 20)
model.Add(y1 + y2 + y3 == 19)
model.Add(z1 + z2 + z3 == 8)
model.Add(x1 + y1 + z1 == 22)
model.Add(x2 + y2 + z2 == 18)
model.Add(x3 + y3 + z3 == 7)

status = solver.Solve(model)

if status == cp_model.FEASIBLE:
    print('x1 = %i' % solver.Value(x1))
    print('x2 = %i' % solver.Value(x2))
    print('x3 = %i' % solver.Value(x3))
    print('y1 = %i' % solver.Value(y1))
    print('y2 = %i' % solver.Value(y2))
    print('y3 = %i' % solver.Value(y3))
    print('z1 = %i' % solver.Value(z1))
    print('z2 = %i' % solver.Value(z2))
    print('z3 = %i' % solver.Value(z3))