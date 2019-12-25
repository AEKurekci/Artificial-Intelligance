from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
import random
import math

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
    print(listOfDifferences)
    return listOfDifferences


while line:
    line = line.strip().split(',')
    income.append(int(line[0]))
    spend.append(int(line[1]))
    line = file.readline()
plt.scatter(income, spend, s=2, marker='o')

listOfCenters = []
for counter in range(K):
    rand = random.randrange(0, len(income))
    listOfCenters.append(rand)
centerOfIncome = []
centerOfSpend = []
for i in listOfCenters:
    centerOfIncome.append(income[i])
    centerOfSpend.append(spend[i])
plt.scatter(centerOfIncome, centerOfSpend, s=2, c='r', marker='o')

for j in range(len(income)):
    clustering(centerOfIncome, centerOfSpend, income[j], spend[j])
plt.show()
exit(0)
