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

K = int(input("Please enter K :"))


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

listOfCenters = []
for counter in range(K):
    rand = random.randrange(0, len(income))
    listOfCenters.append(rand)
centerOfIncome = {}
centerOfSpend = {}
for i, k in enumerate(listOfCenters):
    centerOfIncome[i] = income[i]
    centerOfSpend[i] = spend[i]
    if i == 0:
        color = 'r'
        listX = copy.deepcopy(list(centerOfIncome.values())[i])
        listY = copy.deepcopy(list(centerOfSpend.values())[i])
    elif i == 1:
        color = 'g'
        listX = copy.deepcopy(list(centerOfIncome.values())[i])
        listY = copy.deepcopy(list(centerOfSpend.values())[i])
    elif i == 2:
        color = 'b'
        listX = copy.deepcopy(list(centerOfIncome.values())[i])
        listY = copy.deepcopy(list(centerOfSpend.values())[i])
    elif i == 3:
        color = 'm'
        listX = copy.deepcopy(list(centerOfIncome.values())[i])
        listY = copy.deepcopy(list(centerOfSpend.values())[i])
    elif i == 4:
        color = 'y'
        listX = copy.deepcopy(list(centerOfIncome.values())[i])
        listY = copy.deepcopy(list(centerOfSpend.values())[i])
    plt.scatter(listX, listY, s=2, c=color, marker='o')
print("center of income ", centerOfIncome)

for j in range(len(income)):
    listOFDiff = clustering(centerOfIncome, centerOfSpend, income[j], spend[j])

plt.show()
exit(0)
