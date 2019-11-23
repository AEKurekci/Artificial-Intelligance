# starter code for solving knapsack problem using genetic algorithm
import random

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
elitism = bool(input('Elitism? (Y or N) ' ))


print('\n----------------------------------------------------------')
print('initalizing population')
population = []
for i in range(popSize):
    temp = []
    for j in range(len(w)):
        temp.append(random.randint(0, 1))
    population.append(temp)


print('evaluating fitnesses')
weightDict = {}
selectedParentDict = {}
denominator = 0
for i, chrom in enumerate(population):
    ft = 0
    wt = 0
    for j, gene in enumerate(chrom):
        ft += gene * v[j]
        wt += gene * w[j]
    if wt < c:
        selectedParentDict[i] = chrom
        weightDict[i] = wt
        denominator += wt
    print(i + 1, chrom, ft, wt)


#selection parent
if parentSelection == 1:
    weightOfParent2 = 0
    weightOfParent1 = 0
    while weightOfParent2 == 0:
        selection = random.randint(0, denominator)
        parentCandidates = list(weightDict.values())
        print("selection ", selection)
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
            print("values ", values)
            print("low ", low)
elif parentSelection == 2:
    print("k-Tournament")
else:
    print("Hatalı giriş")

#Crossing-Over
for i in list(weightDict.keys()):
    if weightDict[i] == weightOfParent1:
        parent1 = selectedParentDict[i]
    elif weightDict[i] == weightOfParent2:
        parent2 = selectedParentDict[i]
print("parent1: ", parent1)
print("parent2: ", parent2)








fout.write('chromosome: 101010111000011\n')
fout.write('weight: 749\n')
fout.write('value: 1458')
fout.close() 
