import math
import copy
import matplotlib.pyplot as plt

testFile = open("test.txt", "r")
trainFile = open("train.txt", "r")
testLine = testFile.readline()
testLine = testFile.readline()
test = testLine.strip().split(',')
lastItemOfTest = int(test[-1])
test.pop(-1)

trainLine = trainFile.readline()
trainLine = trainFile.readline()

sumUp = 0
result = 0
listOfDifferences = []
listOfLastTrainItems = []
listOfLastTestItems = []

K = int(input("Please enter the K : "))


def difference(x1, y1):
    return abs(x1 - y1)


tempOfAccuracy = 0
accuracy = {}
for i in range(K):
    accuracy[i + 1] = 0

while testLine:
    listOfDifferences = []
    listOfLastTrainItems = []
    while trainLine:
        train = trainLine.strip().split(',')
        lastItemOfTrain = int(train[-1])
        train.pop(-1)
        for index, value in enumerate(test):
            temp = difference(float(value), float(train[index]))
            temp = temp ** 2
            sumUp += temp
        result = math.sqrt(sumUp)
        listOfDifferences.append(result)
        listOfLastTrainItems.append(lastItemOfTrain)
        sumUp = 0
        trainLine = trainFile.readline()

    listOfSmallest = []
    listOfClasses = []
    counter = 0
    while counter < K:
        tempListOfDifferences = listOfDifferences
        smallest = tempListOfDifferences[0]
        indexOfSmallest = 0
        for i, e in enumerate(tempListOfDifferences):
            if e < smallest:
                smallest = e
                indexOfSmallest = i
        listOfSmallest.append(smallest)
        listOfClasses.append(int(listOfLastTrainItems[indexOfSmallest]))
        listOfDifferences.pop(indexOfSmallest)
        counter += 1

    zero = 0
    one = 0
    two = 0
    three = 0
    listOfClassValues = {}
    dictOfValues = {}
    for l, j in enumerate(listOfClasses):
        if j == 0:
            zero += 1
        elif j == 1:
            one += 1
        elif j == 2:
            two += 1
        elif j == 3:
            three += 1
        listOfClassValues[0] = zero
        listOfClassValues[1] = one
        listOfClassValues[2] = two
        listOfClassValues[3] = three
        dictOfValues[l + 1] = copy.deepcopy(listOfClassValues)
    for z in dictOfValues.keys():
        fittest = 0
        indexOfFittest = 0
        for a, b in dictOfValues[z].items():
            if b > fittest:
                fittest = b
                indexOfFittest = a
            elif b == fittest:
                if listOfClasses[0] == a:
                    fittest = b
                    indexOfFittest = a
        lastItemOfTest = int(lastItemOfTest)
        if lastItemOfTest == indexOfFittest:
            tempOfAccuracyItem = accuracy[z]
            tempOfAccuracyItem += 1
            accuracy[z] = tempOfAccuracyItem

    listOfLastTestItems.append(lastItemOfTest)
    testLine = testFile.readline()
    test = testLine.strip().split(',')
    lastItemOfTest = test[-1]
    test.pop(-1)

    trainFile = open("train.txt", "r")
    trainLine = trainFile.readline()
    trainLine = trainFile.readline()


xAxis = []
yAxis = []
for x, y in accuracy.items():
    y = y / 10.0
    xAxis.append(x)
    yAxis.append(y)
plt.plot(xAxis, yAxis)
plt.xlabel('K Values')
plt.ylabel('Accuracy(%)')
plt.show()
exit(0)
