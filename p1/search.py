# Python3 program to print DFS traversal
# from a given given graph
from collections import defaultdict
import sys
import copy


# This class represents a directed graph using
# adjacency list representation
class GraphDepthFirstSearch:

    # Constructor
    def __init__(self):

        # default dictionary to store graph
        self.graph = defaultdict(list)

        # function to add an edge to graph

    def addEdge(self, u, v):
        self.graph[u].append(v)

        # A function used by DFS

    def DFSUtil(self, v, visited, path):

        # Mark the current node as visited
        # and print it
        visited[v] = True
        path.append(v)

        # Recur for all the vertices
        # adjacent to this vertex
        for i in self.graph[v]:
            if visited[i] == False:
                self.DFSUtil(i, visited, path)

                # The function to do DFS traversal. It uses

    # recursive DFSUtil()
    def DFS(self, v):

        # Mark all the vertices as not visited
        visited = [False] * (len(self.graph))
        path = []
        # Call the recursive helper function
        # to print DFS traversal
        self.DFSUtil(v, visited, path)
        return path

    # This class represents a directed graph
    # using adjacency list representation

class GraphUniformCostSearch:
    dictionaryOfCost = {}
    dictOfTheDic = {}
    record = 1
    def __init__(self):
        self.graph = defaultdict(list)

    def addEdge(self, u, v, cost, lastU):
        if u == self.record:
            self.dictOfTheDic[u - 1] = copy.deepcopy(self.dictionaryOfCost)
            self.record += 1
            self.dictionaryOfCost.clear()
        self.graph[u].append(v)
        self.dictionaryOfCost[v] = cost
        if u == lastU:
            self.dictOfTheDic[u] = copy.deepcopy(self.dictionaryOfCost)

    def UCS(self, source, destination):
        visited = [False] * (len(self.graph))

        queue = {}
        path = []

        queue[source] = source
        visited[source] = True
        shortestEdge = source
        path.append(shortestEdge)
        while queue:
            source = queue[shortestEdge]
            queue.clear()

            for i in self.graph[source]:
                if visited[i] == False:
                    queue[i] = i
            dictOfPathOptions = self.dictOfTheDic[source]
            shortest = 10000
            for i in dictOfPathOptions:
                if dictOfPathOptions[i] < shortest and visited[i] == False:
                    shortest = dictOfPathOptions[i]
                    shortestEdge = i
                if i == destination:
                    shortestEdge = i
                    path.append(shortestEdge)
                    return path
            visited[shortestEdge] = True
            path.append(shortestEdge)
            if shortestEdge == destination:
                return path

class GraphBreathFirstSearch:

        # Constructor
        def __init__(self):
            # default dictionary to store graph
            self.graph = defaultdict(list)
            # function to add an edge to graph
        def addEdge(self, u, v):
            self.graph[u].append(v)

            # Function to print a BFS of graph

        def BFS(self, s):

            # Mark all the vertices as not visited
            visited = [False] * (len(self.graph))

            # Create a queue for BFS
            queue = []
            pathOfBFS = []

            # Mark the source node as
            # visited and enqueue it
            queue.append(s)
            visited[s] = True

            while queue:

                # Dequeue a vertex from
                s = queue.pop(0)
                #print(s, end=" ")
                pathOfBFS.append(s)

                # Get all adjacent vertices of the
                # dequeued vertex s. If a adjacent
                # has not been visited, then mark it
                # visited and enqueue it
                for i in self.graph[s]:
                    if visited[i] == False:
                        queue.append(i)
                        visited[i] = True
            return pathOfBFS

    # Driver code
graphDFS = GraphDepthFirstSearch()
graphBFS = GraphBreathFirstSearch()
graphUCS = GraphUniformCostSearch()
fileIsExist = False
dic = {}
dicValues = {}
dicKeys = {}
indexOfRow = 0
lastU = 0
indexOfValuesDic = 0
fromLastIndexOfEdge = -5
fromLastIndexOfCost = -3
fromFirstIndexOfEdge = 3
line = ""
try:
    fileName = sys.argv[1]
    file = open(fileName, "r")
    line = file.readline()
    fileIsExist = True
    while line:
        vertex = str(line[0])
        dicKeys[vertex] = indexOfRow
        while line[fromLastIndexOfCost]:
            try:
                costOfEdge = int(line[fromLastIndexOfCost])
                edgeForDic = str(line[fromFirstIndexOfEdge])
                if edgeForDic not in dicValues:
                    dicValues[edgeForDic] = indexOfValuesDic
                    indexOfValuesDic += 1
                if costOfEdge > 0:
                    edge = str(line[fromLastIndexOfEdge])
                    graphDFS.addEdge(indexOfRow, dicValues[edge])
                    graphBFS.addEdge(indexOfRow, dicValues[edge])
                    graphUCS.addEdge(indexOfRow, dicValues[edge], costOfEdge, lastU)
            except:
                indexOfRow += 1
                break
            fromLastIndexOfEdge -= 5
            fromLastIndexOfCost -= 5
            fromFirstIndexOfEdge += 5
        lastU = ((fromFirstIndexOfEdge - 3) // 5) - 1 # for determine last index border
        indexOfValuesDic = 0
        fromLastIndexOfEdge = -5
        fromLastIndexOfCost = -3
        fromFirstIndexOfEdge = 3
        line = file.readline()
    file.close()
except:
    print("Please enter a graph file name in the current directory!(.\\file_name)")
    fileIsExist = False

if fileIsExist == True:
    startState = input("Please enter the start state : ")
    goalState = input("Please enter the goal state : ")
    startState = startState.upper()
    goalState = goalState.upper()
    pathOfDFS = graphDFS.DFS(dicKeys[startState])
    pathOfBFS = graphBFS.BFS(dicKeys[startState])
    pathOfUCS = graphUCS.UCS(dicKeys[startState], dicKeys[goalState])
    resultOfDFS = ""
    resultOfBFS = ""
    resultOfUCS = ""

    for iBFS in pathOfBFS:
        if startState == list(dicValues.keys())[list(dicValues.values()).index(iBFS)]:
            resultOfBFS = "BFS : " + list(dicValues.keys())[list(dicValues.values()).index(iBFS)] + ' - '
        elif goalState != list(dicValues.keys())[list(dicValues.values()).index(iBFS)]:
            resultOfBFS += list(dicValues.keys())[list(dicValues.values()).index(iBFS)] + ' - '
        else:
            resultOfBFS += list(dicValues.keys())[list(dicValues.values()).index(iBFS)]
            break

    print(resultOfBFS)

    for iDFS in pathOfDFS:
        if startState == list(dicValues.keys())[list(dicValues.values()).index(iDFS)]:
            resultOfDFS = "DFS : " + list(dicValues.keys())[list(dicValues.values()).index(iDFS)] + ' - '
        elif goalState != list(dicValues.keys())[list(dicValues.values()).index(iDFS)]:
            resultOfDFS += list(dicValues.keys())[list(dicValues.values()).index(iDFS)] + ' - '
        else:
            resultOfDFS += list(dicValues.keys())[list(dicValues.values()).index(iDFS)]
            break
    print(resultOfDFS)

    for iUCS in pathOfUCS:
        if startState == list(dicValues.keys())[list(dicValues.values()).index(iUCS)]:
            resultOfUCS = "UCS : " + list(dicValues.keys())[list(dicValues.values()).index(iUCS)] + ' - '
        elif goalState != list(dicValues.keys())[list(dicValues.values()).index(iUCS)]:
            resultOfUCS += list(dicValues.keys())[list(dicValues.values()).index(iUCS)] + ' - '
        else:
            resultOfUCS += list(dicValues.keys())[list(dicValues.values()).index(iUCS)]
            break
    print(resultOfUCS)
