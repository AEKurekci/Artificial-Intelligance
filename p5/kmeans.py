from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
import random
file = open("data.txt", "r")
line = file.readline()
line = file.readline()
spend = []
income = []

K = int(input("Please enter K :"))

while line:
    line = line.strip().split(',')
    income.append(line[0])
    spend.append(line[1])
    line = file.readline()
plt.scatter(income, spend, s=2, marker='o')

listOfCenters = []
for counter in range(K):
    rand = random.randrange(0, len(income) + 1)
    listOfCenters.append(rand)
tempIncome = []
tempSpend = []
for i in listOfCenters:
    tempIncome.append(income[i])
    tempSpend.append(spend[i])
plt.scatter(tempIncome, tempSpend, s=2, c='r', marker='o')
plt.show()
exit(0)
