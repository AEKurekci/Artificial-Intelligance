def init_Pass(T):
    initList = {}
    for i in T:
        for j in i:
            if j not in initList.keys():
                initList[j] = 1
            else:
                initList[j] += 1
    return initList

def apriori(Transaction, minSup):
    C1 = init_Pass(Transaction)
    F1 =