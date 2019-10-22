from __future__ import print_function
from ortools.sat.python import cp_model

model = cp_model.CpModel()
solver = cp_model.CpSolver()

x1 = model.NewIntVar(1, 4, "x1")
x2 = model.NewIntVar(1, 4, "x2")
x3 = model.NewIntVar(1, 4, "x3")
x4 = model.NewIntVar(1, 4, "x4")

xList = [x1, x2, x3, x4]

y1 = model.NewIntVar(1, 4, "y1")
y2 = model.NewIntVar(1, 4, "y2")
y3 = model.NewIntVar(1, 4, "y3")
y4 = model.NewIntVar(1, 4, "y4")

yList = [y1, y2, y3, y4]

model.AddAllDifferent(yList)