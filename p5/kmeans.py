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

isTrue = False
while not isTrue:
    try:
        K = int(input("Please enter K :"))
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


while line:
    line = line.strip().split(',')
    income.append(int(line[0]))
    spend.append(int(line[1]))
    line = file.readline()
plt.scatter(income, spend, s=2, c='k', marker='o')

listOfCenterX = []
listOfCenterY = []
for counter in range(K):
    randX = random.randrange(sorted(income)[0], sorted(income, reverse=True)[0])
    randY = random.randrange(sorted(spend)[0], sorted(spend, reverse=True)[0])
    listOfCenterX.append(randX)
    listOfCenterY.append(randY)
dictCenterOfIncome = {}
dictCenterOfSpend = {}
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
    plt.scatter(listX, listY, s=2, c=color, marker='o')

for j in range(len(income)):
    listOFDiff = clustering(dictCenterOfIncome, dictCenterOfSpend, income[j], spend[j])
    smallest = listOFDiff[0]
    indexOfSmallest = 0
    for t, z in enumerate(listOFDiff):
        if z < smallest:
            smallest = z
            indexOfSmallest = t
    if indexOfSmallest == 0:
        color = 'r'
        listX = copy.deepcopy(income[j])
        listY = copy.deepcopy(spend[j])
    elif indexOfSmallest == 1:
        color = 'g'
        listX = copy.deepcopy(income[j])
        listY = copy.deepcopy(spend[j])
    elif indexOfSmallest == 2:
        color = 'b'
        listX = copy.deepcopy(income[j])
        listY = copy.deepcopy(spend[j])
    elif indexOfSmallest == 3:
        color = 'm'
        listX = copy.deepcopy(income[j])
        listY = copy.deepcopy(spend[j])
    elif indexOfSmallest == 4:
        color = 'y'
        listX = copy.deepcopy(income[j])
        listY = copy.deepcopy(spend[j])
    plt.scatter(listX, listY, s=2, c=color, marker='o')

plt.show()
exit(0)
