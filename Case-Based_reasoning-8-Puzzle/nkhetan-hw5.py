'''
Created on Oct 5th 2013

@author for 8 puzzle: Shreya, Mukesh

Modified on Oct 2nd 2013

@author for implementing case based reasoning: Khetan, Nihar <nkhetan@indiana.edu>

Usage: 

With every run a local file "cbr_database.pickle" is generated with cases added by solving given problems

NOTE:::: to start fresh DELETE cbr_database.pickle manually so that all previous learnings are erased

'''

import time
import pickle
from pydoc import deque
from heapq import heappush, heappop
from __builtin__ import str
#goalState = []

# Informed search - A*
def informedSearch(initialState, limit, numRuns, choice):
    # List to keep track of visited nodes
    visited = []
    
    
    # path of the tree
    temp_path = [initialState[0]]

    # If empty state, return
    if initialState == []:
        print "No Solution Exists"
        return 
    elif testProcedure(initialState[0]):
        # Check state is goal state and print output
        #outputProcedure(numRuns, initialState[0])
        return temp_path
    elif limit == 0:
        # If limit reached return
        
        return []
    
    # calculate g(n),h(n) and f(n) for the root node
    g_n = 0
    h_n = heuristicFunction(initialState[0], choice)
    f_n = g_n + h_n

    # implement a heap
    heap = []
    
    # push the root, path as well as its f(n) into the heap
    heappush(heap, (f_n, [initialState[0], temp_path]))
    
    while len(heap) > 0:
        # Pop node with highest f(n)
        (cost_unwanted, nodeList) = heappop(heap)
        
        # Glean state and path to state
        n = nodeList[0]
        temp_path = nodeList[1]

        if n not in visited:
            visited.append(n)   # Append state to visited state
            limit -= 1
            numRuns += 1
            if testProcedure(n):    # Test if goal state
                #path = outputProcedure(numRuns, temp_path)
                return temp_path
            elif limit == 0:    # Test if limit reached
                print "Limit reached"
                return []
            
            successors = expandProcedure(n) # Generate successors
            for succ in successors:
                # Calculate f_n for the successor
                g_n = len(temp_path)-1
                h_n = heuristicFunction(succ, choice)
                f_n = g_n + h_n;

                # Push f(n), successor and path to successor to the heap
                heappush(heap, (f_n, [succ, (temp_path + [succ])]))

    print "No Solution Exists"                
    return

def heuristicFunction(currentState, choice):
    
    if choice == "one": # Misplaced Tile hueristic
        noTilesMismatch = 0;
        for i in range(0,len(goalState)):
            # Find mispalced tiles and add to counter
            if (goalState[i] != currentState[i]):
                noTilesMismatch += 1
        return noTilesMismatch

    elif choice == "two":   # Manhatten Distance
        # This should ideally work for any goal statedefined in the program
        posTilesGoal = dict()
        posTilesState = dict()

        # Find position of each node and add to dict ("value":position)
        # for both goal state and current state
        for i in range(0,len(goalState)):
            posTilesGoal[goalState[i]] = i;
            posTilesState[currentState[i]] = i;

        # Counter for sum of manhatten distances
        manhattenDst = 0

        # For each value in current state, find the number of blocks away from
        # it's position in goal state and sum it up
        for i in range(1,len(goalState)):
            # For pairs on the right corner and left corner, we need two additional moves
            if ((posTilesGoal[i] == 2 and posTilesState[i] == 3) or \
                (posTilesGoal[i] == 3 and posTilesState[i] == 2) or \
                (posTilesGoal[i] == 2 and posTilesState[i] == 6) or \
                (posTilesGoal[i] == 6 and posTilesState[i] == 2) or \
                (posTilesGoal[i] == 5 and posTilesState[i] == 6) or \
                (posTilesGoal[i] == 6 and posTilesState[i] == 5)) :
                posTilesGoal[i] += 6
                    
            diff = abs(posTilesGoal[i]-posTilesState[i])
            
            manhattenDst += (diff/3) + (diff%3)
        return manhattenDst
        
def testProcedure(queue):
    if (queue == goalState):
        return True
    else:
        return False
     
def outputProcedure(path):
    #print "Total number of runs=", numRuns
    if (path != []):
        print "Path Cost=", len(path)-1
        
        idx = 0
           
        for i in path:
            
            print "Game State: ", idx
            idx += 1
            print (" " if i[0] == 0 else i[0]) , " " , (" " if i[1] == 0 else i[1]) , " " , (" " if i[2] == 0 else i[2]) 
            print (" " if i[3] == 0 else i[3]) , " " , (" " if i[4] == 0 else i[4]) , " " , (" " if i[5] == 0 else i[5]) 
            print (" " if i[6] == 0 else i[6]) , " " , (" " if i[7] == 0 else i[7]) , " " , (" " if i[8] == 0 else i[8]), "\n"
        
        
# Successor function        
def expandProcedure(state):
    successors = []
    blankPos = 0
    adjacent = []
    # Get position of blank tile
    for i in range(len(state)):
        if state[i] == 0:
            blankPos = i
    
    # Check whether left edge tiles
    if (blankPos % 3 != 2):
        nextPos = blankPos + 1
        adjacent.append(nextPos)

    # Check whether right edge tiles
    if (blankPos % 3 != 0):
        prev = blankPos - 1
        adjacent.append(prev)

    # Check up tile
    if (blankPos > 2):
        up = blankPos - 3
        adjacent.append(up)

    # Check down tile
    if (blankPos < 6):
        down = blankPos + 3
        adjacent.append(down)

    succ = state
    for pos in adjacent:
        succ = list(state)
        
    # Swap tiles and make new state. Add to successor
        if pos >= 0 and pos <= 8:
            temp = succ[blankPos]
            succ[blankPos] = succ[pos]
            succ[pos] = temp
            successors.append(succ)
    return successors
    
# Create state from initial and goal state
def makeState(nw, n, ne, w, c, e, sw, s, se):
    statelist = [nw, n, ne, w, c, e, sw, s, se]
    for i in range(len(statelist)):
    # Replace blank with 0
        if statelist[i] == "blank":
            statelist[i] = 0
    return statelist
    

def testInformedSearch(initialState, goalState, limit):
    '''print "\nHueristic: No of mispalced Tiles"
    t1 = time.time()
    informedSearch ([initialState], limit, 0, "one")
    print "Time taken for Informed Search(Misplaced Tiles): ", (time.time()-t1) ," Seconds"
    print "\nHueristic: Manhatten Distance"'''
    t2 = time.time()
    informedSearch ([initialState], limit, 0, "two")
    print "Time taken for Informed Search(Manhatten Distance): ", (time.time()-t2) ," Seconds"
    return


'''---------------------------------------------------------------------------------------------------------------------------'''
'''-----------------------------------------------------CODE FOR CBR----------------------------------------------------------'''
'''---------------------------------------------------------------------------------------------------------------------------'''
'''New code added here for Case Based Reasoning: @author: Nihar Khetan'''


def getPositionInGoalState(valueOfElement, gstate):
    '''It returns the position of a particular number which is in initial state, in Goal state
    number -> (number,number)'''
    for i in range(3):
        for j in range(3):
            if valueOfElement == gstate[i][j]:
                return (i,j)

def calcEucledianDistance(initialState, gstate):
    '''It calculates Euclidean Distance for 8 Puzzle
    for an initialState Euclidean distance is the sum of moves for each number in initial state, to move it to the respective goal state
    so Heuristic Function 2 is based on Euclidean Distance
    initialState -> pathCost'''
    pathCost = 0
    for i in range(3):
        for j in range(3):
            if int(initialState[i][j]) != 0:                
                if int(initialState[i][j]) != int((gstate)[i][j]):
                    x,y = getPositionInGoalState(initialState[i][j], gstate)
                    pathCost = pathCost + (abs(x-i)+abs(y-j))
    return pathCost

def convertToMatrice(state):
    '''converts the given state to a matrice like it looks for a 8- Puzzle'''
    count = 0
    newArr = [[" "," "," "],[" "," "," "],[" "," "," "]]    
    for i in range(3):
        for j in range(3):            
            newArr[i][j] = state[count]
            count+=1            
    return newArr

def computeSimilarity(I0, I1, G1, G0):
    '''this function computes similarity between given initial and goal states to initial and goal states in case based database
        It uses sum of Manhattan distance : dist(I1-I0) + dist(G1, G0)
        where I0: given initial state I1: initial state from CBR database  
              G0: given goal state    G1: goal state from CBR database
    '''
    scoreI0I1 = calcEucledianDistance(convertToMatrice(I0), convertToMatrice(I1))    
    scoreG0G1 = calcEucledianDistance(convertToMatrice(G0), convertToMatrice(G1))
        
    return (scoreI0I1 + scoreG0G1)

def getKeyForMostSimilar(I1, G1):
    ''' Gets the most similar case from case based reasoning and return the key for the same ''' 
    cbrDb = readFromDict()
    scoreDict = {}
    print ("++-------------------------------------+------------------- CBR Database -------------------+--------------------------------------++")
    print ("\tKey\t\t\t\tInitial State\t\t\t\tGoal State\t\t\t\tSimilarity Score ")
    for key in cbrDb.keys():
        scoreDict[key] = computeSimilarity(I1, cbrDb[key][0], cbrDb[key][len(cbrDb[key])-1], G1)       
        print ("\t%s\t\t\t\t%s\t\t%s\t\t%s " %(str(key), str(cbrDb[key][0]), str(cbrDb[key][len(cbrDb[key])-1]), str(computeSimilarity(I1, cbrDb[key][0], cbrDb[key][len(cbrDb[key])-1], G1))))
    return ((sorted(scoreDict.items(), key=lambda x:x[1]))[0][0], (sorted(scoreDict.items(), key=lambda x:x[1]))[0][1]) 
    
def getKey(initial, goal):
    ''' Gets the key form case based reasoning and returns the same for a given initial and goal states'''
    cbrDb = readFromDict()
    for key in cbrDb.keys():
        if ((cbrDb[key][0] == initial) and (cbrDb[key][len(cbrDb[key])-1] == goal)):
            return key
    return -1
    
def checkIfPresent(initial, goal):
    ''' Checks if initial and goal states are exactly present in the case based reasoning --> returns boolean'''
    cbrDB = readFromDict()     
    for eachProblem in cbrDB.values() :        
        if ((eachProblem[0] == initial) and (eachProblem[len(eachProblem)-1] == goal)):
            return True        
    return False   

def checkIfPresentInAnyState(initial, goal):
    '''Function checks if given initial and goal exists in any of sub paths of solutions in CBR database
    list, list -> boolean'''
    cbrDB = readFromDict()   
    print ("Exact Match not found thus checking all states of all paths stored in CBR Database")
    
    for eachProblem in cbrDB.values() :        
        if ((initial in eachProblem) and (goal in eachProblem)):
            if (eachProblem.index(initial) < (eachProblem.index(goal))):                
                return True  
            else:
                return False          
    return False   

def computePathFromAnyOtherState(initial, goal):
    '''Try to look at sub-paths of solutions in CBR database and if it is found returns the same 
    initial state, goal state --> list '''
    cbrDB = readFromDict()    
    counter = 0
    for eachProblem in cbrDB.values() :        
        if ((initial in eachProblem) and (goal in eachProblem)):
            if (eachProblem.index(initial) < (eachProblem.index(goal))):
                print ("MATCH FOUND in a path for Case Based Reasoning Database")
                print ("Key for case matched : " + str(counter))  
                print ("Similarity Score = 0\n")              
                return eachProblem[eachProblem.index(initial):eachProblem.index(goal)+1]  
            else:
                return []
        counter += 1
    return []      

def readFromDict():
    '''Reader to read the cases stored in case based reasoning and returns the dictionery
    ---> returns a dictionery'''
    with open('cbr_database.pickle', 'rb') as handle:
        savedCases = pickle.load(handle)
        return savedCases

def writeToDict(caseToWrite):
    '''Opens the case bases reasoning and write a new case to it, while persisting the older ones
    ---> does not return anything'''
    current = readFromDict()
    current.update(caseToWrite)
    with open('cbr_database.pickle', 'wb') as handle:
        pickle.dump(current, handle)
    return

  

def testCaseBasedSearch(listOfProblems): 
    '''Function which goes through each problem in list of problems and solves it using Case Based Search''' 
      
    for i in range(len(listOfProblems)):        
        initial1 = listOfProblems[i][0]
        goal1 = listOfProblems[i][1]
        global goalState
        print ("++---------------------------------------------------------------------------------------------------------------------------------------------++")
        print ("++---------------------------------------------------------------------------------------------------------------------------------------------++\n")
        
        print("Solving Problem : " + str(i+1))
        print("Given Initial State : " + str(initial1))
        print("Given Goal State : " + str(goal1) + "\n")
        '''If CBR database is empty solve the first problem and store it'''
        cbrCheck = readFromDict();
        if (cbrCheck == {}):
            print("+-+-  Empty CBR Database Solving from scratch  -+-+")
            goalState = goal1
            pathSearched = informedSearch ([initial1], 20000, 0, "two")
            outputProcedure(pathSearched)
            print("++-----Appending new Path to CBR Database------++\n")
            cbrDB = readFromDict()
            dictToAppend = {0:pathSearched}
            writeToDict(dictToAppend)                    
           
        else:
            '''Case to check if initial state and goal state matches exactly :: BEST CASE'''     
            if (checkIfPresent(initial1,goal1)):            
                key = getKey(initial1,goal1)
                
                goalState = goal1
                print ("Exact Match Found in CBR at Key : " + str(key))
                print ("\tSimilarity Score = 0\n")            
                outputProcedure(readFromDict()[key])
            elif (checkIfPresentInAnyState(initial1, goal1) == True):            
                outputProcedure(computePathFromAnyOtherState(initial1, goal1))
            else:
                print ("\nInitial State and Goal State not found in sub paths hence computing SIMILARITY SCORES ::")
                (key, score) = getKeyForMostSimilar(initial1,goal1)
                
                if (score < 9):
                    #use case based reasoning
                    print ("\nScore less than THRESHOLD thus applying CBR")
                    print ("\tMost Similar Key : " + str(key) + "\tSimilarity Score : " + str(score))
                    cbrDB = readFromDict()
                    #goal state is I0
                    
                    goalState = cbrDB[key][0]
                                    
                    pathSearchedI0toI1 = informedSearch ([initial1], 20000, 0, "two")
                    print("\tPath From I0 to I1 : " + str(pathSearchedI0toI1))
                    pathSearchedI1toG1 = cbrDB[key]
                    print("\tPath From I1 to G1 (CBR) : " + str(pathSearchedI1toG1))                
                    goalState = goal1
                    pathSearchedG1toG0 = informedSearch ([cbrDB[key][len(cbrDB[key])-1]], 20000, 0, "two")
                    print("\tPath From G1 to G0 : " + str(pathSearchedG1toG0))                
                    pathSearched = pathSearchedI0toI1 + pathSearchedI1toG1[1:-1] + pathSearchedG1toG0
                    print("\nCombined Path I0 --> I1 --> G1 --> G0")                
                    outputProcedure(pathSearched)
                    print("++-----Appending new Path to CBR Database------++\n")
                    dictToAppend = {(cbrDB.keys()[len(cbrDB.keys())-1]+1):pathSearched}
                    writeToDict(dictToAppend)
                else:
                    #find solution from scratch and add it to Case Based Reasoning Database
                    print ("\nComputed Score : " + str(score) + ", Which is Greater than THRESHOLD : 8")                
                    print("Solving from scratch using A* Search\n")
                    goalState = goal1
                    pathSearched = informedSearch ([initial1], 20000, 0, "two")
                    outputProcedure(pathSearched)
                    print("++-----Appending new Path to CBR Database------++\n")
                    cbrDB = readFromDict()                       
                    if (cbrDB.keys() == []):
                        dictToAppend = {0:pathSearched}
                        writeToDict(dictToAppend)                    
                    else:
                        dictToAppend = {(cbrDB.keys()[len(cbrDB.keys())-1]+1):pathSearched}
                        writeToDict(dictToAppend)         
  
              

def generateTestProblems(listOfProblems):
    '''This function generated a set of Random Problems.
        I have followed approach 1 where I give a predefined set of problems as input
        so this acts as a dummy function'''

    testCaseBasedSearch(listOfProblems)
  
# Main()
if __name__ == "__main__":
    global goalState
    goalState = []
    print "<<<<  ::::::      CASE BASED REASONING TO SOLVE 8 PUZZLE      ::::::  >>>>\n"
    try:
        with open('cbr_database.pickle', 'rb') as handle:
            savedCases = pickle.load(handle)
            print ("printing the CBR Database")
            for eachKey in savedCases.keys():
                print (str(eachKey) + " : " + str(savedCases[eachKey]))                
            print("")
    except IOError:        
        emptyDict = {}
        with open('cbr_database.pickle', 'wb') as handle:
            pickle.dump(emptyDict, handle)
    
    
    '''Given sample list of problems'''
    listOfProblems = [
                      [makeState("blank", 5, 3, 2, 1, 6, 4, 7, 8), makeState(1, 2, 3, 4, 5, 6, 7, 8, "blank")],
                      [makeState("blank", 3, 6, 5, 7, 8, 2, 1, 4), makeState(1, 2, 3, 4, 5, 6, 7, "blank", 8)],
                      [makeState(3, 6, "blank", 5, 7, 8, 2, 1, 4), makeState(1, 2, 3, 4, 5, 6, 7, 8, "blank")],
                      [makeState("blank", 2, 5, 3, 1, 6, 4, 7, 8), makeState(1, 2, 3, 4, 5, 6, 7, 8, "blank")],
                      [makeState(3, 2, 5, "blank", 1, 6, 4, 7, 8), makeState(1, "blank", 3, 4, 2, 5, 7, 8, 6)],
                      [makeState("blank", 2, 1, 5, 3, 6, 4, 7, 8), makeState(1, 2, 3, 4, 5, 6, 7, 8, "blank")],
                      [makeState(2, 5, "blank", 4, 6, 3, 7, 1, 8), makeState(1, 2, 3, 4, 5, 6, 7, "blank", 8)],
                      [makeState(2, 6, 5, 4, "blank", 3, 7, 1, 8), makeState(1, 2, 3, 4, 5, 6, 7, 8, "blank")],
                      [makeState(1, "blank", 3, 5, 2, 6, 4, 7, 8), makeState(1, 2, 3, 4, 8, 5, 7, "blank", 6)],
                      [makeState("blank", 2, 3, 1, 5, 6, 4, 7, 8), makeState(2, 6, 5, 4, "blank", 3, 7, 1, 8)],
                      [makeState(2, 3, 8, 1, 6, 5, 4, 7, "blank"), makeState("blank", 2, 3, 1, 5, 6, 4, 7, 8)],
                      [makeState(2, 5, 3, 4, "blank", 8, 6, 1, 7), makeState(1, 2, 3, 4, 5, 6, 7, 8, "blank")],
                      [makeState(3, 8, 5, 1, 6, 7, 4, 2, "blank"), makeState(1, 2, 3, 4, 5, 6, 7, 8, "blank")],
                      [makeState(3, 8, 5, 1, "blank", 6, 4, 2, 7), makeState(1, 2, 3, 4, "blank", 5, 7, 8, 6)],
                      [makeState(3, 8, 5, 1, 6, "blank", 4, 2, 7), makeState(1, 2, 3, 4, 8, 5, "blank", 7, 6)],
                      [makeState(1, 3, 5, "blank", 8, 6, 4, 2, 7), makeState(1, 2, 3, 4, 5, "blank", 7, 8, 6)],
                      [makeState(3, 8, 5, 1, 6, "blank", 4, 2, 7), makeState(1, 2, 3, 4, 8, 5, 7, "blank", 6)],
                      [makeState("blank", 3, 5, 1, 8, 6, 4, 2, 7), makeState(1, 2, 3, 4, 5, 6, 7, 8, "blank")],
                      [makeState("blank", 3, 5, 1, 8, 6, 4, 2, 7), makeState(1, 2, 3, 4, 5, 6, 7, 8, "blank")],
                      [makeState(2, 5, 3, 4, "blank", 8, 6, 1, 7), makeState(1, 2, 3, 4, 5, 6, "blank", 7, 8)]
                      ]
    t1 = time.time()
    generateTestProblems(listOfProblems)
    t2 = time.time()
    print "\n\nTime taken for solving by CBR: ", (t2-t1), " Seconds"
    
   