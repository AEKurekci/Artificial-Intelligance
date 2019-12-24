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

K = int(input("Please enter the K "))


def difference(x1, y1):
    return abs(x1 - y1)


accuracy = 0
while testLine:
    listOfDifferences = []
    listOfLastTrainItems = []
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

    listOfSmallest = []
    listOfClasses = []
    counter = 0
    while counter < K:
        tempListOfDifferences = listOfDifferences
        smallest = tempListOfDifferences[0]
        indexOfSmallest = 0
        for i, e in enumerate(tempListOfDifferences):
            if e <= smallest:
                smallest = e
                indexOfSmallest = i
        listOfSmallest.append(smallest)
        listOfClasses.append(listOfLastTrainItems[indexOfSmallest])
        listOfDifferences.pop(indexOfSmallest)
        counter += 1

    zero = 0
    one = 0
    two = 0
    three = 0
    listOfClassValues = []
    for j in listOfClasses:
        if j == 0:
            zero += 1
        elif j == 1:
            one += 1
        elif j == 2:
            two += 1
        elif j == 3:
            three += 1
    listOfClassValues.append(zero)
    listOfClassValues.append(one)
    listOfClassValues.append(two)
    listOfClassValues.append(three)
    print("class list ", listOfClasses)
    fittest = 0
    indexOfFittest = 0
    for a, b in enumerate(listOfClassValues):
        if b >= fittest:
            fittest = b
            indexOfFittest = a
    lastItemOfTest = int(lastItemOfTest)
    if lastItemOfTest == indexOfFittest:
        print("accuracy is increased")
        accuracy += 1

    listOfLastTestItems.append(lastItemOfTest)
    testLine = testFile.readline()
    test = testLine.strip().split(',')
    lastItemOfTest = test[-1]
    test.pop(-1)

    trainFile = open("train.txt", "r")
    trainLine = trainFile.readline()
    trainLine = trainFile.readline()

#print("differences ", listOfDifferences)
#print("trains ", listOfLastTrainItems)
#print("test ", listOfLastTestItems)
print("accuracy ", accuracy)
print("differences ", len(listOfDifferences))
print("trains ", len(listOfLastTrainItems))
print("test ", len(listOfLastTestItems))
