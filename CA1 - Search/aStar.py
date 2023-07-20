from copy import deepcopy
import time
import heapq

ALPHA = 1.7

def getInput():
    f = open('input3.txt', 'r')

    #edges
    line = [int(x) for x in f.readline().split()]
    n ,m = line[0], line[1]
  
    edges = [[] for x in range(n)]
    for i in range(m):
        line = [int(x) for x in f.readline().split()]
        x, y = line[0], line[1]
        edges[x-1].append(y-1)
        edges[y-1].append(x-1)

    #saabolobur
    h = int(f.readline())
    saabolobur = [False for x in range(n)]
    sabIndex = [int(x) for x in f.readline().split()]
    for sab in sabIndex:
        saabolobur[sab-1] = True
    
    #morids and recipes
    recipes = [False for x in range(n)]
    moridRecipes = [ {'doesExist' : False} for x in range(n)]
    for i in range(n):
        moridRecipes[i]['recipes'] = []
    moridsCount = int(f.readline())
    moridLocs = []
    moridCountInEachLoc = [0 for x in range(n)]
    for i in range(moridsCount):
        line = [int(x) - 1 for x in f.readline().split()]
        loc = line.pop(0) 
        moridLocs.append(loc)
        recipeCount = line.pop(0) 
        moridRecipes[loc]['doesExist'] = True
        moridRecipes[loc]['recipes'].append ([x for x in line]) 
        moridCountInEachLoc[loc] += 1

        for rec in line:
            recipes[rec] = True

    morids = {}
    for loc in moridLocs:
        morids[str(loc)] = []
        for i in range(moridCountInEachLoc[loc]):
            morids[str(loc)].append(False)


    startLoc = int(f.readline()) - 1
    return n, edges, saabolobur, recipes, morids , startLoc, moridRecipes, moridCountInEachLoc

#######################################################################################c
class State:

    def __init__(self, n, loc, morids):
        self.saaboloburVisited = [0 for x in range(n)] 
        self.morids = morids
        self.recipesVisited = [False for x in range(n)]
        self.nodesCount = n
        self.loc = loc
        self.father = None
        self.remainingTime = 0
        self.cost = 0
        self.F = -1

    def __lt__(self, other):
        return self.cost < other.cost

    def inheritFromFather(self, father):
        self.father = father
        self.morids = {key: list(val) for key, val in father.morids.items()}
        self.recipesVisited = list(father.recipesVisited)
        self.saaboloburVisited = list(father.saaboloburVisited)
        self.cost = int(father.cost)

    def goalTest(self):
        for x in self.morids.keys():
            for morid in self.morids[x]:
                if morid == False:
                    return False
        return True

    def isSameState(self , curState):
        if (self.morids == curState.morids and self.remainingTime == curState.remainingTime and self.loc == curState.loc and
            self.saaboloburVisited == curState.saaboloburVisited and self.recipesVisited == curState.recipesVisited):
            if (self.F > curState.F):
                return False
            return True
        return False

    def updateSaabolobur(self, loc):
        self.remainingTime = self.saaboloburVisited[loc]
        self.saaboloburVisited[loc] += 1

    def updateRecipes(self, loc):
        self.recipesVisited[loc] = True

    def updateMorids(self, loc, moridRecipes):
        satisfiedMoridCount = 0
        for recipeList in moridRecipes:
            seenRecipeCount = 0
            for recipe in recipeList:
                if self.recipesVisited[recipe] == False:
                    break
                else:
                    seenRecipeCount += 1
            if seenRecipeCount == len(recipeList):
                self.morids[str(loc)][satisfiedMoridCount] = True
                satisfiedMoridCount += 1

    def reduceRemainingTime(self):
        self.remainingTime -= 1

    def increaseCost(self):
        self.cost += 1

    def caclHeuristic(self,recipes, moridCountInEachLoc):
        h = 0
        for loc in self.morids.keys():
            for morid in self.morids[loc]:
                if morid == False:
                    h += 1
                    break
        for rec in recipes:
            if rec == True and self.recipesVisited[rec] == False and moridCountInEachLoc[rec] == 0:
                h += 1
        return h

    def calcFfunction(self, recipes, moridCountInEachLoc):
        self.F = self.cost + ALPHA * self.caclHeuristic(recipes, moridCountInEachLoc)
        return self.F







###############################################################################

def isInVisited(currentState, visited):
    for f in visited:
        if (f.isSameState(currentState)):
            return True
    return False

def printOutput(goal, visitedStatesCount):
    print('The numbers of visited states is: ',visitedStatesCount)
    print('Final Cost is: ', goal.cost)
    path = []
    while(goal != None):
        path.append(goal.loc + 1)
        goal = goal.father
    finalPath = ''
    for i in range(len(path)):
        j = len(path) - 1 - i
        if(j != 0):
            temp = str(path[j]) + ' -> '
            finalPath += temp
        else:
            finalPath += str(path[j])

    print("Path: ",finalPath)

def Astar(n, edges, saabolobur, recipes, morids , startLoc, moridRecipes, moridCountInEachLoc):
    visitedStatesCount = 0
    startState = State(n, startLoc, morids)
    visitedStatesCount += 1
    visited = []
    if (saabolobur[startLoc]):
        startState.updateSaabolobur()
    if (recipes[startLoc]):
        startState.updateRecipes()
    if (moridCountInEachLoc[startLoc] > 0):
        startState.updateMorids(startLoc, moridRecipes[startLoc]['recipes'])
    if (startState.goalTest() == True):
        return startState, visitedStatesCount
    visited.append(startState)
    currentF = startState.calcFfunction(recipes, moridCountInEachLoc)
    heapList = [(currentF, startState)]
    heapq.heapify(heapList)

    while (len(heapList)):
        currentF, currentState = heapq.heappop(heapList)
        if (currentState.goalTest() == True):
            return currentState, visitedStatesCount
        if (currentState.remainingTime == 0):
            for childLoc in edges[currentState.loc]:
                childState = State(n, childLoc, morids)
                childState.inheritFromFather(currentState)
                childState.increaseCost()
                visitedStatesCount += 1
                if (saabolobur[childLoc]):
                    childState.updateSaabolobur(childLoc)
                if (recipes[childLoc]):
                    childState.updateRecipes(childLoc)
                if (moridCountInEachLoc[childLoc] > 0):
                    childState.updateMorids(childLoc, moridRecipes[childLoc]['recipes'])
                childF = childState.calcFfunction(recipes, moridCountInEachLoc)
                if (isInVisited(childState, visited) == False):
                    visited.append(childState)
                    heapq.heappush(heapList, (childF, childState))
        else:
            currentState.reduceRemainingTime()
            currentState.increaseCost()
            currentF =  currentState.caclHeuristic(recipes, moridCountInEachLoc) + currentState.cost
            heapq.heappush(heapList, (currentF, currentState))

 ##################################################################################

n, edges, saabolobur, recipes, morids , startLoc, moridRecipes, moridCountInEachLoc = getInput()
startState = State(n, startLoc, morids)

start = time.time()
goal, visitedStatesCount = Astar(n, edges, saabolobur, recipes, morids , startLoc, moridRecipes , moridCountInEachLoc)
print(f'A* time: {time.time() - start}')

printOutput(goal, visitedStatesCount)
