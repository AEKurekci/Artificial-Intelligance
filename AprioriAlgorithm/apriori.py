def init_Pass(T):
    initList = {}
    for i in T:
        for j in i:
            if j not in initList.keys():
                initList[j] = 1
            else:
                initList[j] += 1
    sortedInitList = {}
    """
    listOfKeys = initList.keys()
    listOfKeys =list(listOfKeys)
    listOfKeys.sort()
    print(listOfKeys)
    listOfKeys = listOfKeys.sort()
    print(listOfKeys)

    for key in listOfKeys:
        sortedInitList[key] = initList[key]
    initList.clear()
    """
    print(initList)
    for b in sorted(initList.keys(),reverse=True):
       sortedInitList[b] = initList[b]
    print(sortedInitList)
    return sortedInitList


def candidate_gen(F):
    C = {}
    for i in F:
        if len(i) == 1:
            print("candidate")
    pass


def apriori(Transaction, minSup):
    C1 = init_Pass(Transaction)
    #print(C1)
    allF = []
    Frequent = {}
    for i, j in C1.items():
        if (float(j) / float(len(Transaction))) > minSup:
            Frequent[i] = j
    allF.append(Frequent)
    while len(Frequent) != 0:
        Candidates = candidate_gen(Frequent)

file = open("transactions.csv", "r")
line = file.readline()
allList = []
while line:
    listOfTransaction = line.strip(' ').split(',')
    print(listOfTransaction)
    allList.append(listOfTransaction)
    line = file.readline()
apriori(allList, 0.3)