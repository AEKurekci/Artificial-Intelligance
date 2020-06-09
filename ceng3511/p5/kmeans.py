from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
import random
import math
import copy

file = open("data.txt", "r")
line = file.readline()
line = file.readline()
spend = []
income = []

listRX = []
listGX = []
listBX = []
listMX = []
listYX = []
listRY = []
listGY = []
listBY = []
listMY = []
listYY = []

listX = []
listY = []

color = 'k'

listOfCenterX = []
listOfCenterY = []

dictCenterOfIncome = {}
dictCenterOfSpend = {}

isTrue = False
while not isTrue:
    try:
        K = int(input("Please enter K : "))
        if 0 < K <= 5:
            isTrue = True
        else:
            print("K value should be smaller than 5 and greater than 0 !\n")
            isTrue = False
    except:
        print("Please enter numeric K!\n")


def difference(val1, val2):
    return abs(val1 - val2)


def clustering(centersX, centersY, x, y):
    listOfDifferences = []
    for a in range(len(centersX)):
        diffX = difference(x, centersX[a])
        diffY = difference(y, centersY[a])
        diffX = diffX ** 2
        diffY = diffY ** 2
        sumOFDiff = diffX + diffY
        sumOFDiff = math.sqrt(sumOFDiff)
        listOfDifferences.append(sumOFDiff)
    return listOfDifferences


def newMean():
    global listX, listY, color
    for i, j in enumerate(listOfCenterX):
        if i == 0:
            if len(listRX) != 0 and len(listRY) != 0:
                color = 'r'
                meanX = (sorted(listRX)[0] + sorted(listRX)[-1]) / 2
                meanY = (sorted(listRY)[0] + sorted(listRY)[-1]) / 2
                listOfCenterX.pop(i)
                listOfCenterX.insert(i, meanX)
                listOfCenterY.pop(i)
                listOfCenterY.insert(i, meanY)
                dictCenterOfIncome[i] = meanX
                dictCenterOfSpend[i] = meanY
                listX = copy.deepcopy(listOfCenterX[i])
                listY = copy.deepcopy(listOfCenterY[i])
            else:
                color = 'r'
                listX = copy.deepcopy(listOfCenterX[i])
                listY = copy.deepcopy(listOfCenterY[i])
        elif i == 1:
            if len(listGX) != 0 and len(listGY) != 0:
                color = 'g'
                meanX = (sorted(listGX)[0] + sorted(listGX)[-1]) / 2
                meanY = (sorted(listGY)[0] + sorted(listGY)[-1]) / 2
                listOfCenterX.pop(i)
                listOfCenterX.insert(i, meanX)
                listOfCenterY.pop(i)
                listOfCenterY.insert(i, meanY)
                dictCenterOfIncome[i] = meanX
                dictCenterOfSpend[i] = meanY
                listX = copy.deepcopy(listOfCenterX[i])
                listY = copy.deepcopy(listOfCenterY[i])
            else:
                color = 'g'
                listX = copy.deepcopy(listOfCenterX[i])
                listY = copy.deepcopy(listOfCenterY[i])
        elif i == 2:
            if len(listBX) != 0 and len(listBY) != 0:
                color = 'b'
                meanX = (sorted(listBX)[0] + sorted(listBX)[-1]) / 2
                meanY = (sorted(listBY)[0] + sorted(listBY)[-1]) / 2
                listOfCenterX.pop(i)
                listOfCenterX.insert(i, meanX)
                listOfCenterY.pop(i)
                listOfCenterY.insert(i, meanY)
                dictCenterOfIncome[i] = meanX
                dictCenterOfSpend[i] = meanY
                listX = copy.deepcopy(listOfCenterX[i])
                listY = copy.deepcopy(listOfCenterY[i])
            else:
                color = 'b'
                listX = copy.deepcopy(listOfCenterX[i])
                listY = copy.deepcopy(listOfCenterY[i])
        elif i == 3:
            if len(listMX) != 0 and len(listMY) != 0:
                color = 'm'
                meanX = (sorted(listMX)[0] + sorted(listMX)[-1]) / 2
                meanY = (sorted(listMY)[0] + sorted(listMY)[-1]) / 2
                listOfCenterX.pop(i)
                listOfCenterX.insert(i, meanX)
                listOfCenterY.pop(i)
                listOfCenterY.insert(i, meanY)
                dictCenterOfIncome[i] = meanX
                dictCenterOfSpend[i] = meanY
                listX = copy.deepcopy(listOfCenterX[i])
                listY = copy.deepcopy(listOfCenterY[i])
            else:
                color = 'm'
                listX = copy.deepcopy(listOfCenterX[i])
                listY = copy.deepcopy(listOfCenterY[i])
        elif i == 4:
            if len(listYX) != 0 and len(listYY) != 0:
                color = 'y'
                meanX = (sorted(listYX)[0] + sorted(listYX)[-1]) / 2
                meanY = (sorted(listYY)[0] + sorted(listYY)[-1]) / 2
                listOfCenterX.pop(i)
                listOfCenterX.insert(i, meanX)
                listOfCenterY.pop(i)
                listOfCenterY.insert(i, meanY)
                dictCenterOfIncome[i] = meanX
                dictCenterOfSpend[i] = meanY
                listX = copy.deepcopy(listOfCenterX[i])
                listY = copy.deepcopy(listOfCenterY[i])
            else:
                color = 'y'
                listX = copy.deepcopy(listOfCenterX[i])
                listY = copy.deepcopy(listOfCenterY[i])
        plt.scatter(listX, listY, s=10, c=color, marker='o')


def colorPoints(centerX, centerY, inc, spe):
    # coloring other points
    global listX, listY, color
    for j in range(len(inc)):
        listOFDiff = clustering(centerX, centerY, inc[j], spe[j])
        smallest = listOFDiff[0]
        indexOfSmallest = 0
        for t, z in enumerate(listOFDiff):
            if z < smallest:
                smallest = z
                indexOfSmallest = t
        if indexOfSmallest == 0:
            color = 'r'
            listRX.append(inc[j])
            listRY.append(spe[j])
            listX = copy.deepcopy(inc[j])
            listY = copy.deepcopy(spe[j])
        elif indexOfSmallest == 1:
            color = 'g'
            listGX.append(inc[j])
            listGY.append(spe[j])
            listX = copy.deepcopy(inc[j])
            listY = copy.deepcopy(spe[j])
        elif indexOfSmallest == 2:
            color = 'b'
            listBX.append(inc[j])
            listBY.append(spe[j])
            listX = copy.deepcopy(inc[j])
            listY = copy.deepcopy(spe[j])
        elif indexOfSmallest == 3:
            color = 'm'
            listMX.append(inc[j])
            listMY.append(spe[j])
            listX = copy.deepcopy(inc[j])
            listY = copy.deepcopy(spe[j])
        elif indexOfSmallest == 4:
            color = 'y'
            listYX.append(inc[j])
            listYY.append(spe[j])
            listX = copy.deepcopy(inc[j])
            listY = copy.deepcopy(spe[j])
        plt.scatter(listX, listY, s=2, c=color, marker='o')


#spend and income values plotting initially
while line:
    line = line.strip().split(',')
    income.append(int(line[0]))
    spend.append(int(line[1]))
    line = file.readline()
plt.scatter(income, spend, s=2, c='k', marker='o')

#initial centers randomly
for counter in range(K):
    randX = random.randrange(sorted(income)[0], sorted(income, reverse=True)[0])
    randY = random.randrange(sorted(spend)[0], sorted(spend, reverse=True)[0])
    listOfCenterX.append(randX)
    listOfCenterY.append(randY)

#plotting centers
for i, k in enumerate(listOfCenterX):
    dictCenterOfIncome[i] = listOfCenterX[i]
    dictCenterOfSpend[i] = listOfCenterY[i]
    if i == 0:
        color = 'r'
        listX = copy.deepcopy(list(dictCenterOfIncome.values())[i])
        listY = copy.deepcopy(list(dictCenterOfSpend.values())[i])
    elif i == 1:
        color = 'g'
        listX = copy.deepcopy(list(dictCenterOfIncome.values())[i])
        listY = copy.deepcopy(list(dictCenterOfSpend.values())[i])
    elif i == 2:
        color = 'b'
        listX = copy.deepcopy(list(dictCenterOfIncome.values())[i])
        listY = copy.deepcopy(list(dictCenterOfSpend.values())[i])
    elif i == 3:
        color = 'm'
        listX = copy.deepcopy(list(dictCenterOfIncome.values())[i])
        listY = copy.deepcopy(list(dictCenterOfSpend.values())[i])
    elif i == 4:
        color = 'y'
        listX = copy.deepcopy(list(dictCenterOfIncome.values())[i])
        listY = copy.deepcopy(list(dictCenterOfSpend.values())[i])
    plt.scatter(listX, listY, s=10, c=color, marker='o')


gameOver = False
gameOverCounter = 0
while not gameOver:
    tempDictCenterOfIncomes = copy.deepcopy(dictCenterOfIncome)
    tempDictCenterOfSpends = copy.deepcopy(dictCenterOfSpend)
    colorPoints(dictCenterOfIncome, dictCenterOfSpend, income, spend)
    newMean()
    for control in list(dictCenterOfSpend.keys()):
        if tempDictCenterOfIncomes[control] == dictCenterOfIncome[control] and tempDictCenterOfSpends[control] == dictCenterOfSpend[control]:
            gameOverCounter += 1
    if gameOverCounter == K:
        gameOver = True
    else:
        gameOverCounter = 0

with PdfPages("plot.pdf") as pdf:
    plt.figure(figsize=(10, 10))
    plt.xlabel('Income')
    plt.ylabel('Spend')
    plt.title('K Means Clustering')
    colorPoints(dictCenterOfIncome, dictCenterOfSpend, income, spend)
    newMean()
    pdf.savefig()
    plt.close()
exit(0)
