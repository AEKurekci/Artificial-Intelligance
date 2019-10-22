from __future__ import print_function
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
solver.Solve(model)
solver.Value(z1 + z2 + z3 < 6)

print(z1.Index())
print(z2.Index())
print(z3.Index())
print(x1.Index())
print(x2.Index())
print(x3.Index())
print(y1.Index())
print(y2.Index())
print(y3.Index())






