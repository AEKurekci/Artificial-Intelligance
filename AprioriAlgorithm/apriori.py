def init_Pass(T):
    initList = {}
    for i in T:
        for j in i:
            if j not in initList.keys():
                initList[j] = 1
            else:
                initList[j] += 1
    sortedInitList = {}
    for key in initList.keys():
        sortedInitList[key] = initList[key]
    initList.clear()
    return sortedInitList


def candidate_gen(F):
    C = {}
    for i in F:
        if len(i) == 1:
            print("candidate")
    pass


def apriori(Transaction, minSup):
    C1 = init_Pass(Transaction)
    allF = []
    Frequent = {}
    for i, j in C1.items():
        if (j / len(Transaction)) > minSup:
            Frequent[i] = j
    allF.append(Frequent)
    while len(Frequent) != 0:
        Candidates = candidate_gen(Frequent)