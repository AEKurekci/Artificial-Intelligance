import math

testFile = open("test.txt", "r")
trainFile = open("train.txt", "r")
testLine = testFile.readline()
testLine = testFile.readline()
test = testLine.strip().split(',')
lastItemOfTest = test[-1]
test.pop(-1)

trainLine = trainFile.readline()
trainLine = trainFile.readline()

sumUp = 0
result = 0
listOfDifferences = []
listOfLastTrainItems = []
listOfLastTestItems = []

K = input("Please enter the K ")


def difference(x1, y1):
    return abs(x1 - y1)


while testLine:
    while trainLine:
        train = trainLine.strip().split(',')
        lastItemOfTrain = train[-1]
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
    listOfLastTestItems.append(lastItemOfTest)
    testLine = testFile.readline()
    test = testLine.strip().split(',')
    lastItemOfTest = test[-1]
    test.pop(-1)
    trainFile = open("train.txt", "r")
    trainLine = trainFile.readline()
    trainLine = trainFile.readline()

print("differences ", listOfDifferences)
print("trains ", listOfLastTrainItems)
print("test ", listOfLastTestItems)

print("differences ", len(listOfDifferences))
print("trains ", len(listOfLastTrainItems))
print("test ", len(listOfLastTestItems))
