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
    notSame = False
    keyList = list(F.keys())
    for i, j in enumerate(keyList):
        j = j.split(',')
        keyList.pop(i)
        keyList.insert(i, j)
    for f1 in keyList:
        for f2 in keyList:
            if f1[-1] < f2[-1]:
                if len(f1) > 1:#it is just for after first specifying candidate
                    for itemIndex in range(len(f1) - 1):
                        if f1[itemIndex] != f2[itemIndex]:
                            notSame = True
                            break
                if notSame:
                    notSame = False
                    break
                else:
                    f1.append(f2[-1])
                    copyf1 = copy.deepcopy(f1)
                    Cand.append(copyf1)
                    f1.pop(-1)
    #elimination for not in subset of C.
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
    transactionCount = len(Transaction)
    allF = []
    Frequent = {}
    candidateCountList = []
    for i, j in C1.items():
        if (float(j) / float(transactionCount)) > minSup:
            Frequent[i] = j
    while len(list(Frequent.keys())) > 0:
        allF.append(copy.deepcopy(Frequent))
        Candidates = candidate_gen(Frequent)
        biggerThanMinSupCandidateIndex = []
        for index, can in enumerate(Candidates):
            candidateCount = 0
            for t in Transaction:
                transLastIndex = len(t) - 1
                canLastIndex = len(can) - 1
                equalityCount = 0
                while canLastIndex >= 0 and transLastIndex >= 0:
                    if can[canLastIndex] == t[transLastIndex]:
                        canLastIndex -= 1
                        transLastIndex = len(t) - 1
                        equalityCount += 1
                    else:
                        transLastIndex -= 1
                if equalityCount == len(can):
                    candidateCount += 1
            if (float(candidateCount) / float(transactionCount)) > float(minSup):
                biggerThanMinSupCandidateIndex.append(index)
            candidateCountList.append(candidateCount)
        tempCandidates = []
        for a in biggerThanMinSupCandidateIndex:
            tempCandidates.append(copy.deepcopy(Candidates[a]))
        Candidates.clear()
        Candidates = copy.deepcopy(tempCandidates)
        tempCandidates.clear()
        Frequent.clear()
        for indexOfCand, Cand in enumerate(Candidates):
            item = ""
            for i in range(len(Cand)):
                item += Cand[i]
                if i != len(Cand) - 1:
                    item += ','
            Frequent[item] = candidateCountList[biggerThanMinSupCandidateIndex[indexOfCand]]
        candidateCountList.clear()
        biggerThanMinSupCandidateIndex.clear()
    return allF



file = open("transactions.txt", "r")
line = file.readline()
allList = []
minimumSupport = 0.3
while line:
    listOfTransaction = line.strip().split(',')#strip to get rid of \n
    #for is here to get rid of spaces
    for i, j in enumerate(listOfTransaction):
        j = j.lstrip(' ')
        listOfTransaction.pop(i)
        listOfTransaction.insert(i, j)
    allList.append(listOfTransaction)
    line = file.readline()
    try:
        minimumSupport = float(line)
        break
    except:
        pass

allFrequencies = apriori(allList, minimumSupport)
print("All Frequencies: ", allFrequencies)
outputFile = open("output.txt", "w")
outputFile.write(str(allFrequencies))