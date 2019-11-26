# starter code for solving knapsack problem using genetic algorithm
import random
import copy

fc = open('./c.txt', 'r')
fw = open('./w.txt', 'r')
fv = open('./v.txt', 'r')
fout = open('./out.txt', 'w')


c = int(fc.readline())
w = []
v = []
for line in fw:
    w.append(int(line))
for line in fv:
    v.append(int(line))

print('Capacity :', c)
print('Weight :', w)
print('Value : ', v)

popSize = int(input('Size of population : '))
genNumber = int(input('Max number of generation : '))
print('\nParent Selection\n---------------------------')
print('(1) Roulette-wheel Selection')
print('(2) K-Tournament Selection')
parentSelection = int(input('Which one? '))
if parentSelection == 2:
    k = int(input('k=? (between 1 and ' + str(len(w)) + ') '))

print('\nN-point Crossover\n---------------------------')
n = int(input('n=? (between 1 and ' + str(len(w) - 1) + ') '))

print('\nMutation Probability\n---------------------------')
mutProb = float(input('prob=? (between 0 and 1) '))

print('\nSurvival Selection\n---------------------------')
print('(1) Age-based Selection')
print('(2) Fitness-based Selection')
survivalSelection = int(input('Which one? '))
what = True
while what:
    elitism = input('Elitism? (Y or N) ')
    elitism.lower()
    if elitism == "y":
        elitism = True
        what = False
    elif elitism == "n":
        elitism = False
        what = False

print('\n----------------------------------------------------------')
print('initalizing population')
population = []
for i in range(popSize):
    temp = []
    for j in range(len(w)):
        temp.append(random.randint(0, 1))
    population.append(temp)

ageBased = {}
age = 1
fittestForElitism = 0
print('evaluating fitnesses')
weightDict = {}#!
allWeightDict = {}
allFitnessDict = {}
selectedParentDict = {}#!
fitnessValueDict = {}
denominator = 0
for i, chrom in enumerate(population):
    ft = 0
    wt = 0
    for j, gene in enumerate(chrom):
        ft += gene * v[j]
        wt += gene * w[j]
    allWeightDict[i] = wt
    allFitnessDict[i] = ft
    ageBased[i] = age
    if wt <= c:
        if ft >= fittestForElitism:
            fittestForElitism = ft
            indexOfElitism = i
        selectedParentDict[i] = copy.deepcopy(chrom)
        weightDict[i] = wt
        denominator += ft
        fitnessValueDict[i] = ft
    print(i + 1, chrom, ft, wt)

#selection parent
#--Roulette-Wheel Selection
selectedChild = []
if parentSelection == 1:
    weightOfParent2 = 0
    weightOfParent1 = 0
    popSizeTemp = copy.deepcopy(popSize)
    weightOfAllParentsDict = {}
    indexOfweightOfAllParentsDict = 0
    indexOfChild = []
    while popSizeTemp > 0:
        popSizeTemp -= 1
        selection = random.randint(0, denominator)
        #low limit
        low = 0
        for keys, values in fitnessValueDict.items():
            if selection >= low and selection < (low + values):
                weightOfAllParentsDict[indexOfweightOfAllParentsDict] = values
                indexOfweightOfAllParentsDict += 1
                indexOfChild.append(keys)
                break
            else:
                low += values

    for o in indexOfChild:
        selectedChild.append(population[o])
#--K-Tournament Selection
elif parentSelection == 2:
    print("k-Tournament")
    kSelParents = {}
    kSelindexesPar = []
    popSizeTemp = copy.deepcopy(popSize)
    while popSizeTemp > 0:
        popSizeTemp -= 1
        kTemp = k
        while kTemp > 0:
            randIndex = random.randint(0, popSize - 1)
            if randIndex not in kSelindexesPar:
                kSelParents[randIndex] = copy.deepcopy(population[randIndex])
                kSelindexesPar.append(randIndex)
                kTemp -= 1
        biggestW = copy.deepcopy(allWeightDict[kSelindexesPar[0]])
        closestWeight = abs(biggestW - c)
        for indexOfKTour in kSelindexesPar:
            if abs(allWeightDict[indexOfKTour] - c) <= closestWeight:
                closestWeight = abs(allWeightDict[indexOfKTour] - c)
                indexOfClosest = indexOfKTour
        for indexW in list(allWeightDict.keys()):
            if indexW == indexOfClosest:
                selectedChild.append(kSelParents[indexW])
        kSelindexesPar.clear()
        kSelParents.clear()
else:
    print("Hatalı giriş")

print(selectedChild)

#Crossing-Over
sizeOfChild = len(selectedChild)
while sizeOfChild > 0:
    parent1 = selectedChild.pop(sizeOfChild - 1)
    sizeOfChild -= 1
    parent2 = selectedChild.pop(sizeOfChild - 1)
    sizeOfChild -= 1
    virtualList = []
    index = 0
    nTemp = n
    while nTemp < len(parent1):
        virtualList.append(parent1.pop(nTemp - 1))
        geneOfParent2 = parent2.pop(nTemp - 1)
        parent1.insert(nTemp - 1, geneOfParent2)
        parent2.insert(nTemp - 1, virtualList[index])
        index += 1
        nTemp += 1
    selectedChild.insert(sizeOfChild + 1, parent2)
    if sizeOfChild == 0:
        selectedChild.insert(sizeOfChild - 1, parent1)#tek taneli popülasyonlarda
    else:
        selectedChild.insert(sizeOfChild + 2, parent1)#çift taneli popülasyonlarda


#Mutation
sizeOfChild = len(selectedChild)
while sizeOfChild > 0:
    if random.random() <= mutProb:
        flip = random.randrange(0, 14, 1)
        theChild = selectedChild[sizeOfChild - 1]
        print(theChild)
        if theChild[flip] == 0:
            theChild.pop(flip)
            theChild.insert(flip, 1)
        else:
            theChild.pop(flip)
            theChild.insert(flip, 0)
        print(theChild)
        selectedChild.pop(sizeOfChild - 1)
        selectedChild.insert(sizeOfChild - 1, theChild)
    sizeOfChild -= 1

#placed new generation
allWeightDictNew = {}
allFitnessDictNew = {}
fittestForElitismNew = 0
for iNew, chromosome in enumerate(selectedChild):
    ftNew = 0
    wtNew = 0
    for jNew, gene in enumerate(chromosome):
        ftNew += gene * v[jNew]
        wtNew += gene * w[jNew]
    if wtNew <= c:
        if ftNew >= fittestForElitismNew:
            fittestForElitismNew = ftNew
            indexOfElitismNew = iNew
    allWeightDictNew[iNew] = wtNew
    allFitnessDictNew[iNew] = ftNew
    print(iNew + 1, chromosome, ftNew, wtNew)



oldest = 0
for k in ageBased.keys():
    if ageBased[oldest] <= ageBased[k]:
        older = oldest
        oldest = k
    elif ageBased[older] <= ageBased[k]:
        older = k

if survivalSelection == 1:
    print("--Age-Based Survival Selection--")
    population.pop(older)
    population.insert(older, parent1)
    population.pop(oldest)
    population.insert(oldest, parent2)

elif survivalSelection == 2:
    print("--Fitness-Based Survival Selection--")
    kickCandidatesW = []
    kickCandidatesWNew = []
    kickCandidatesF = []
    kickCandidatesFNew = []

    #if elitism:


    for i, item in allWeightDict.items():
        if item > c:
            kickCandidatesW.append(item)

    for i, item in allWeightDictNew.items():
        if item > c:
            kickCandidatesWNew.append(item)

    for i, item in allFitnessDict.items():
        kickCandidatesF.append(item)

    kickCandidatesF.sort()  # ascending
    kickCandidatesW.sort(reverse=True)  # descanding

    kickCandidatesWNew.sort(reverse=True)
    popSizeTemp = popSize
    print("KickCandidatesW: ", kickCandidatesW)
    print("KickCandidatesF: ", kickCandidatesF)
    print("KickCandidatesWNew: ", kickCandidatesWNew)
    print("populasyon: ", population)
    while popSizeTemp > 0:
        if len(kickCandidatesW) > 0:
            for i, item in allWeightDict.items():
                if item == kickCandidatesW[0]:
                    if population[i] != "null":
                        population.pop(i)
                        ageBased.pop(i)
                        population.insert(i, "null")
                        kickCandidatesW.pop(0)
                        break
        elif len(kickCandidatesWNew) > 0:
            for i, item in allWeightDictNew.items():
                if item == kickCandidatesWNew[0]:
                    if selectedChild[i] != "null":
                        selectedChild.pop(i)
                        selectedChild.insert(i, "null")
                        kickCandidatesWNew.pop(0)
                        break
        elif len(kickCandidatesF) > 0:
            for i, item in allFitnessDict.items():
                if item == kickCandidatesF[0]:
                    if population[i] != "null":
                        population.pop(i)
                        ageBased.pop(i)
                        population.insert(i, "null")
                        kickCandidatesF.pop(0)
                        break
        popSizeTemp -= 1

    print("KickCandidatesW: ", kickCandidatesW)
    print("KickCandidatesF: ", kickCandidatesF)
    print("KickCandidatesWNew: ", kickCandidatesWNew)
    print("KickCandidatesFNew: ", kickCandidatesFNew)
    print("population: ", population)
    print("selected Child: ", selectedChild)




fout.write('chromosome: 101010111000011\n')
fout.write('weight: 749\n')
fout.write('value: 1458')
fout.close() 
