import copy

def init_Pass(T):
    initList = {}
    for i in T:
        for j in i:
            if j not in initList.keys():
                initList[j] = 1
            else:
                initList[j] += 1
    sortedInitList = {}
    for b in sorted(initList.keys()):
       sortedInitList[b] = initList[b]
    return sortedInitList


def candidate_gen(F):
    Cand = []
    print(F)
    notSame = False
    keyList = list(F.keys())
    for i, j in enumerate(keyList):
        j = j.split(',')
        keyList.pop(i)
        keyList.insert(i, j)
    for f1 in keyList:
        for f2 in keyList:
            if f1[-1] < f2[-1]:
                if len(f1) > 1:
                    for itemIndex in range(0, len(f1)):
                        if f1[itemIndex] != f2[itemIndex]:
                            notSame = True
                            break
                if notSame:
                    break
                else:
                    f1.append(f2[-1])
                    copyf1 = copy.deepcopy(f1)
                    Cand.append(copyf1)
                    f1.pop(-1)

    for i, j in enumerate(Cand):
        counter = len(j) - 1
        while counter >= 0:
            tempItem = j.pop(counter)
            if j not in keyList:
                Cand.pop(i)
            else:
                j.insert(counter, tempItem)
            counter -= 1
    return Cand


def apriori(Transaction, minSup):
    C1 = init_Pass(Transaction)
    print("C1: ", C1)
    allF = []
    Frequent = {}
    for i, j in C1.items():
        if (float(j) / float(len(Transaction))) > minSup:
            Frequent[i] = j
    print("F1: ", Frequent)
    allF.append(Frequent)
    Candidates = candidate_gen(Frequent)
    print("Cand: ", Candidates)


file = open("transactions.csv", "r")
line = file.readline()
allList = []
while line:
    listOfTransaction = line.strip().split(',')#strip to get rid of \n
    #for is here to get rid of spaces
    for i, j in enumerate(listOfTransaction):
        j = j.lstrip(' ')
        listOfTransaction.pop(i)
        listOfTransaction.insert(i, j)
    allList.append(listOfTransaction)
    line = file.readline()

apriori(allList, 0.3)