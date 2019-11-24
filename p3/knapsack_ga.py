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
elitism = bool(input('Elitism? (Y or N) '))


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
print('evaluating fitnesses')
weightDict = {}
allWeightDict = {}
selectedParentDict = {}
denominator = 0
unfittest = 0
for i, chrom in enumerate(population):
    ft = 0
    wt = 0
    ageBased[i] = random.randrange(0, 10, 1)
    for j, gene in enumerate(chrom):
        ft += gene * v[j]
        wt += gene * w[j]
    allWeightDict[i] = wt
    if wt <= c:
        selectedParentDict[i] = copy.deepcopy(chrom)
        weightDict[i] = wt
        denominator += wt
    else:
        if allWeightDict[unfittest] <= allWeightDict[i]:
            unfittest2 = unfittest
            unfittest = i
        elif allWeightDict[unfittest2] <= allWeightDict[i]:
            unfittest2 = i
    print(i + 1, chrom, ft, wt)
print("selected Parents: ", selectedParentDict)
print("ageBased: ", ageBased)

#selection parent
if parentSelection == 1:
    weightOfParent2 = 0
    weightOfParent1 = 0
    while weightOfParent2 == 0:
        parentCandidates = list(weightDict.values())
        if weightOfParent1 != 0:
            parentCandidates.remove(weightOfParent1)
            denominator -= weightOfParent1
        selection = random.randint(0, denominator)
        indexOfCandidates = list(weightDict.keys())
        #removing selected parent from candidates list
        print("selection ", selection)
        #low limit
        low = 0
        for values in parentCandidates:
            if selection >= low and selection < (low + values):
                if weightOfParent1 == 0:
                    weightOfParent1 = values
                    break
                elif weightOfParent2 == 0:
                    weightOfParent2 = values
                    break
            else:
                low += values
    for ind in list(weightDict.keys()):
        if weightDict[ind] == weightOfParent1:
            parent1 = selectedParentDict[ind]
        elif weightDict[ind] == weightOfParent2:
            parent2 = selectedParentDict[ind]
elif parentSelection == 2:
    print("k-Tournament")
    kSelParents = {}
    kSelindexesPar = []
    while k >= 0:
        randIndex = random.randint(0, popSize)
        if randIndex not in kSelindexesPar:
            kSelParents[randIndex] = copy.deepcopy(population[randIndex])
            kSelindexesPar.append(randIndex)
            k -= 1
    biggestW = copy.deepcopy(allWeightDict[kSelindexesPar[0]])
    for indexOfKTour in kSelindexesPar:
        if allWeightDict[indexOfKTour] >= biggestW:
            secondBiggestW = biggestW
            biggestW = copy.deepcopy(allWeightDict[indexOfKTour])
        elif allWeightDict[indexOfKTour] >= secondBiggestW:
            secondBiggestW = copy.deepcopy(allWeightDict[indexOfKTour])
    for indexW in list(allWeightDict.keys()):
        if allWeightDict[indexW] == biggestW:
            parent1 = kSelParents[indexW]
        elif allWeightDict[indexW] == secondBiggestW:
            parent2 = kSelParents[indexW]
else:
    print("Hatalı giriş")
print(kSelParents)
print("parent1: ", parent1)
print("parent2: ", parent2)

#Crossing-Over
virtualList = []
index = 0
while n < len(parent1):
    virtualList.append(parent1.pop(n))
    parent1.insert(n, parent2.pop(n))
    parent2.insert(n, virtualList[index])
    index += 1
    n += 1
#Mutation
if random.random() <= n:
    flip = random.randrange(0, 14, 1)
    print("flip", flip)
    if random.random() < 0.5:
        if parent1[flip] == 0:
            parent1.pop(flip)
            parent1.insert(flip, 1)
        else:
            parent1.pop(flip)
            parent1.insert(flip, 0)
    else:
        if parent2[flip] == 0:
            parent2.pop(flip)
            parent2.insert(flip, 1)
        else:
            parent2.pop(flip)
            parent2.insert(flip, 0)

#placed new generation
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
    population.pop(unfittest)
    population.insert(unfittest, parent1)
    population.pop(unfittest2)
    population.insert(unfittest2, parent2)


print("older: ", older)
print("oldest: ", oldest)
print("unfit: ", unfittest)
print("unfit2: ", unfittest2)
print(population)

fout.write('chromosome: 101010111000011\n')
fout.write('weight: 749\n')
fout.write('value: 1458')
fout.close() 
