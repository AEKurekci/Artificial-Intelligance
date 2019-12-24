import math

testFile = open("test.txt", "r")
trainFile = open("train.txt", "r")
test = testFile.readline()
test = testFile.readline()
test = test.strip().split()

train = testFile.readline()
train = testFile.readline()
train = train.strip().split()

sumup = 0
listOfdifferences = []


def difference(x1, y1):
    return abs(x1 - y1)


for index, value in enumerate(test):
    sumup += difference(int(test[index]), int(train[index]))**2
listOfdifferences.append(math.sqrt(sumup))
