# starter code for solving knapsack problem using genetic algorithm
import random
import copy
import matplotlib.pyplot as plt

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
isTrue = False
while not isTrue:
    popSize = input('Size of population : ')
    try:
        popSize = int(popSize)
        isTrue = True
    except:
        isTrue = False
isTrue = False
while not isTrue:
    genNumber = input('Max number of generation : ')
    try:
        genNumber = int(genNumber)
        isTrue = True
    except:
        isTrue = False

print('\nParent Selection\n---------------------------')
print('(1) Roulette-wheel Selection')
print('(2) K-Tournament Selection')
isTrue = False
while not isTrue:
    parentSelection = input('Which one? ')
    try:
        parentSelection = int(parentSelection)
        if parentSelection == 1:
            isTrue = True
        elif parentSelection == 2:
            while not isTrue:
                k = input('k=? (between 1 and ' + str(len(w)) + ') ')
                try:
                    k = int(k)
                    if 0 < k <= len(w):
                        isTrue = True
                    else:
                        isTrue = False
                except:
                    isTrue = False
    except:
        isTrue = False

print('\nN-point Crossover\n---------------------------')
isTrue = False
while not isTrue:
    n = input('n=? (between 1 and ' + str(len(w) - 1) + ') ')
    try:
        n = int(n)
        if 0 < n <= len(w):
            isTrue = True
        else:
            isTrue = False
    except:
        isTrue = False
print('\nMutation Probability\n---------------------------')
isTrue = False
while not isTrue:
    mutProb = input('probability=? (between 0 and 1)')
    try:
        mutProb = float(mutProb)
        if 0 <= mutProb <= 1:
            isTrue = True
        else:
            isTrue = False
    except:
        isTrue = False
print('\nSurvival Selection\n---------------------------')
print('(1) Age-based Selection')
print('(2) Fitness-based Selection')
isTrue = False
while not isTrue:
    survivalSelection = input('Which one? ')
    try:
        survivalSelection = int(survivalSelection)
        if survivalSelection == 1:
            isTrue = True
        elif survivalSelection == 2:
            isTrue = True
        else:
            isTrue = False
    except:
        isTrue = False
isTrue = True
while isTrue:
    elitism = input('Elitism? (Y or N) ')
    elitism.lower()
    if elitism == "y":
        elitism = True
        isTrue = False
    elif elitism == "n":
        elitism = False
        isTrue = False

print('\n----------------------------------------------------------')
print('initalizing population')
population = []
for i in range(popSize):
    temp = []
    for j in range(len(w)):
        temp.append(random.randint(0, 1))
    population.append(temp)
forVisualFitnessAxes = []
forVisualGenAxes = []
forVisualGenNumber = genNumber
fitnessValueTheBest = 0
ageBased = {}
for i in range(popSize):
    ageBased[i] = 1
fittestForElitism = 0
print('evaluating fitnesses')
while genNumber > 0:
    allWeightDict = {}
    allFitnessDict = {}
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
        if wt <= c:
            if ft >= fittestForElitism:
                fittestForElitism = ft
                indexOfElitism = i
                weightOftheBest = wt
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

    sizeOfChild = len(selectedChild)
    #Crossing-Over
    if sizeOfChild != 0:
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
                if theChild[flip] == 0:
                    theChild.pop(flip)
                    theChild.insert(flip, 1)
                else:
                    theChild.pop(flip)
                    theChild.insert(flip, 0)
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
                    weightOftheBestNew = wtNew

            allWeightDictNew[iNew] = wtNew
            allFitnessDictNew[iNew] = ftNew
            print(iNew + 1, chromosome, ftNew, wtNew)




        #Elitism
        if fittestForElitism == 0 and fittestForElitismNew == 0:
            theBest = []
            fitnessValueTheBest = 0
            theWeight = 0
        elif fittestForElitismNew > fittestForElitism:
            theBest = selectedChild[indexOfElitismNew]
            indexOfTheBest = indexOfElitismNew
            fitnessValueTheBest = fittestForElitismNew
            theWeight = weightOftheBestNew
        else:
            theBest = population[indexOfElitism]
            indexOfTheBest = indexOfElitism
            fitnessValueTheBest = fittestForElitism
            theWeight = weightOftheBest
        print("The Best: ", theBest)
        print("index of the best: ", indexOfTheBest)


        if survivalSelection == 1:
            print("--Age-Based Survival Selection--")
            for i, value in ageBased.items():
                if elitism:
                    if indexOfTheBest == i:
                        for j in range(15):
                            if population[i][j] != theBest[j]:
                                population.pop(i)
                                population.insert(i, selectedChild[i])
                                break
                    else:
                        population.pop(i)
                        population.insert(i, selectedChild[i])
                        ageBased[i] = 0
                else:
                    population.pop(i)
                    population.insert(i, selectedChild[i])
                    ageBased[i] = 0
            selectedChild.clear()


        elif survivalSelection == 2:
            print("--Fitness-Based Survival Selection--")
            kickCandidatesW = []
            kickCandidatesWNew = []
            kickCandidatesF = []
            kickCandidatesFNew = []

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

            for i in range(len(population)):
                if population[i] == "null":
                    population.pop(i)
                    for j in range(len(selectedChild)):
                        if selectedChild[j] != "null":
                            population.insert(i, selectedChild.pop(j))
                            selectedChild.insert(j, "null")
                            ageBased[i] = 0
                            break
            selectedChild.clear()
    else:
        print("the best doesn't found")
        fitnessValueTheBest = 0
        theWeight = 0
        theBest.clear()
    #placement is done
    for i, value in ageBased.items():
        ageBased[i] = value + 1
    genNumber -= 1
    print("ages: ", ageBased)
    print("Generation Number", genNumber)
    forVisualFitnessAxes.append(fitnessValueTheBest)

thechromosome = ""
for i in theBest:
    thechromosome += str(i)
weight = theWeight
theValue = fitnessValueTheBest

print(forVisualFitnessAxes)
for i in range(1, forVisualGenNumber + 1):
    forVisualGenAxes.append(i)
print(forVisualGenAxes)

plt.plot(forVisualGenAxes, forVisualFitnessAxes)
plt.show()


fout.write('chromosome: ' + thechromosome)
fout.write('\n')
fout.write('weight: ' + str(weight))
fout.write('\n')
fout.write('value: ' + str(theValue))
fout.close()
