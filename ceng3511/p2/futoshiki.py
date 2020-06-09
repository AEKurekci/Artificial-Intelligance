from ortools.sat.python import cp_model

model = cp_model.CpModel()
solver = cp_model.CpSolver()
def futushiki(equality, biggerThan):
    A1 = model.NewIntVar(1, 4, "A1")
    A2 = model.NewIntVar(1, 4, "A2")
    A3 = model.NewIntVar(1, 4, "A3")
    A4 = model.NewIntVar(1, 4, "A4")

    AList = [A1, A2, A3, A4]

    model.AddAllDifferent(AList)

    B1 = model.NewIntVar(1, 4, "B1")
    B2 = model.NewIntVar(1, 4, "B2")
    B3 = model.NewIntVar(1, 4, "B3")
    B4 = model.NewIntVar(1, 4, "B4")

    BList = [B1, B2, B3, B4]

    model.AddAllDifferent(BList)

    C1 = model.NewIntVar(1, 4, "C1")
    C2 = model.NewIntVar(1, 4, "C2")
    C3 = model.NewIntVar(1, 4, "C3")
    C4 = model.NewIntVar(1, 4, "C4")

    CList = [C1, C2, C3, C4]

    model.AddAllDifferent(CList)

    D1 = model.NewIntVar(1, 4, "D1")
    D2 = model.NewIntVar(1, 4, "D2")
    D3 = model.NewIntVar(1, 4, "D3")
    D4 = model.NewIntVar(1, 4, "D4")

    DList = [D1, D2, D3, D4]

    model.AddAllDifferent(DList)

    #Adding columns as all different

    col1 = [A1, B1, C1, D1]
    col2 = [A2, B2, C2, D2]
    col3 = [A3, B3, C3, D3]
    col4 = [A4, B4, C4, D4]

    model.AddAllDifferent(col1)
    model.AddAllDifferent(col2)
    model.AddAllDifferent(col3)
    model.AddAllDifferent(col4)

    allModelValues = [A1, B1, C1, D1, A2, B2, C2, D2, A3, B3, C3, D3, A4, B4, C4, D4]

    #equality comparison
    while equality:
        for i in allModelValues:
            if str(i) == equality[0]:
                model.Add(i == equality[1])
                equality.remove(equality[0])
                equality.remove(equality[0])
    #bigger comparison
    while biggerThan:
        for i in allModelValues:
            if str(i) == biggerThan[0]:
                for j in allModelValues:
                    if str(j) == biggerThan[1] and str(i) != str(j):
                        model.Add(i > j)
                        biggerThan.remove(biggerThan[0])
                        biggerThan.remove(biggerThan[0])
                        break
                if len(biggerThan) == 0:
                    break

    #opening the output file
    outputFile = open("futoshiki_output.txt", "w")

    status = solver.Solve(model)

    if status == cp_model.FEASIBLE:
        outputFile.writelines(str(solver.Value(A1)) + ", " + str(solver.Value(A2)) + ", " + str(solver.Value(A3)) + ", " + str(solver.Value(A4)) + "\n")
        outputFile.writelines(str(solver.Value(B1)) + ", " + str(solver.Value(B2)) + ", " + str(solver.Value(B3)) + ", " + str(solver.Value(B4)) + "\n")
        outputFile.writelines(str(solver.Value(C1)) + ", " + str(solver.Value(C2)) + ", " + str(solver.Value(C3)) + ", " + str(solver.Value(C4)) + "\n")
        outputFile.writelines(str(solver.Value(D1)) + ", " + str(solver.Value(D2)) + ", " + str(solver.Value(D3)) + ", " + str(solver.Value(D4)))
inputFile = open("futoshiki_input.txt", "r")
line = inputFile.readline()

equality = []
biggerThan = []

while line:
    #deleting \n at the end of the line and separeted values by coma
    line = line.strip().split(",")
    try:
        equality.append(line[0])
        equality.append(int(line[1]))
    except:
        #in any case line[0] already appended so we must pop it
        equality.pop()
        biggerThan.append(line[0])
        #deleting empty of the second value
        secondValue = line[1]
        secondValue = secondValue[1:]
        #deleted
        biggerThan.append(secondValue)
    line = inputFile.readline()
#CALLING METHOD
futushiki(equality, biggerThan)
