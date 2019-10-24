from ortools.sat.python import cp_model

model = cp_model.CpModel()
solver = cp_model.CpSolver()
def Kakuro(borders, outputFile):
    #x row values
    x1 = model.NewIntVar(0, 9, "x1")
    x2 = model.NewIntVar(0, 9, "x2")
    x3 = model.NewIntVar(0, 9, "x3")

    xList = [x1, x2, x3]
    #x row values add as all diffirent
    model.AddAllDifferent(xList)

    #y row values
    y1 = model.NewIntVar(0, 9, "y1")
    y2 = model.NewIntVar(0, 9, "y2")
    y3 = model.NewIntVar(0, 9, "y3")

    yList = [y1, y2, y3]
    #y row values add as all diffirent
    model.AddAllDifferent(yList)
    #z row values
    z1 = model.NewIntVar(0, 9, "z1")
    z2 = model.NewIntVar(0, 9, "z2")
    z3 = model.NewIntVar(0, 9, "z3")

    zList = [z1, z2, z3]
    #x row values add as all diffirent
    model.AddAllDifferent(zList)

    firstColumn = [x1, y1, z1]
    secondColumn = [x2, y2, z2]
    thirdColumn = [x3, y3, z3]
    #all columns added to model as all different
    model.AddAllDifferent(firstColumn)
    model.AddAllDifferent(secondColumn)
    model.AddAllDifferent(thirdColumn)

    model.Add(x1 + x2 + x3 == borders[3])
    model.Add(y1 + y2 + y3 == borders[4])
    model.Add(z1 + z2 + z3 == borders[5])
    model.Add(x1 + y1 + z1 == borders[0])
    model.Add(x2 + y2 + z2 == borders[1])
    model.Add(x3 + y3 + z3 == borders[2])

    #model solves
    status = solver.Solve(model)

    if status == cp_model.FEASIBLE:
        outputFile.writelines(str(borders[3]) + ", " + str(solver.Value(x1)) + ", " + str(solver.Value(x2)) + ", " + str(solver.Value(x3)) + "\n")
        outputFile.writelines(str(borders[4]) + ", " + str(solver.Value(y1)) + ", " + str(solver.Value(y2)) + ", " + str(solver.Value(y3)) + "\n")
        outputFile.writelines(str(borders[5]) + ", " + str(solver.Value(z1)) + ", " + str(solver.Value(z2)) + ", " + str(solver.Value(z3)))

file = open("kakuro_input.txt", "r")
line = file.readline()
lineInt = []

outputFile = open("kakuro_output.txt", "w")
outputFile.writelines("x, " + line)
while line:
    line = line.strip().split(",")
    for i in line:
        lineInt.append(int(i))
    line = file.readline()
Kakuro(lineInt, outputFile)
