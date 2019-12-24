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


def difference(x1, y1):
    print("difference ", abs(x1 - y1))
    return abs(x1 - y1)


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
    listOfLastTestItems.append(lastItemOfTest)
    listOfLastTrainItems.append(lastItemOfTrain)
    print("result ", result)
    listOfDifferences.append(result)
    sumUp = 0
    trainLine = trainFile.readline()

