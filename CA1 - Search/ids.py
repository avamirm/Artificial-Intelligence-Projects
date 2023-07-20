from collections import deque
from copy import deepcopy
import time

def getInput():
    f = open('input.txt', 'r')

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

def DFS(startState, n, edges, saabolobur, recipes, morids , moridRecipes, depth, moridCountInEachLoc):
    stack = deque()
    stack.append((startState, 0))
    visitedStatesCount = 1
    while (len(stack)):
        currentState, curDepth = stack.pop()
        if (curDepth > depth):
              continue
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
                if (childState.goalTest() == True):
                    return True, childState, visitedStatesCount
                stack.append((childState, curDepth + 1))
        else:
            currentState.reduceRemainingTime()
            stack.append((currentState, curDepth + 1))
    return False, None, visitedStatesCount
        
    

def IDS(startState, n, edges, saabolobur, recipes, morids , startLoc, moridRecipes , moridCountInEachLoc):
    visitedStatesCount = 1
    if (saabolobur[startLoc]):
        startState.updateSaabolobur()
    if (recipes[startLoc]):
        startState.updateRecipes()
    if (moridCountInEachLoc[startLoc] > 0):
        startState.updateMorids(startLoc, moridRecipes[startLoc]['recipes'])
    if (startState.goalTest() == True):
       return startState, visitedStatesCount
    findAnswer = False
    depth = 1
    while (True):
        startStateCpy = deepcopy(startState)
        findAnswer, goal, visitedStatesCount = DFS(startStateCpy, n, edges, saabolobur, recipes, morids , moridRecipes, depth, moridCountInEachLoc)
        if findAnswer:
            return goal, visitedStatesCount
        depth += 1
 ##################################################################################

n, edges, saabolobur, recipes, morids , startLoc, moridRecipes, moridCountInEachLoc = getInput()
startState = State(n, startLoc, morids)

start = time.time()
goal, visitedStatesCount = IDS(startState, n, edges, saabolobur, recipes, morids , startLoc, moridRecipes , moridCountInEachLoc)
print(f'IDS time: {time.time() - start}')

printOutput(goal, visitedStatesCount)