import copy
import numpy as np
from itertools import combinations
import csv

def bruteForceCoverSolution(faceMatrix,numberOfVertices):
    listOfSolution = []
    vertArr = [(i + 1) for i in range(numberOfVertices)]
    #looping through each solution size
    for i in range(2,numberOfVertices+1):
        #looping through each solution choice
        for solArr in list(combinations(vertArr,i)):
            #checks if this solArr is a solution 
            if solChecker(solArr,faceMatrix):
                #if it is adds it to the arr
                listOfSolution.append(solArr)
    #creates a coverage sol arr
    coverSolution = []
    #loops through all solutions
    for solution in listOfSolution:
        #takes the first one and compares the length
        if len(solution) == len(listOfSolution[0]):
            #if it is the same length then it is added to the solutions
            coverSolution.append(solution)
    #returns the list of coverSolutions
    return coverSolution

def distanceProblemCalc(faceMatrix, solutionSize, power):
    listOfSolution = []

    ####Kevin's code for distance matrix
    maxVert = np.max(faceMatrix)
    ###Creating the Dictionary of each face that touches each vertex
    vertexDictOfTouchedFaces = {}

    for nextVertex in range(maxVert):
        vertexDictOfTouchedFaces[nextVertex+1] = []
    
    ## Fill in the dictionary
    for currentFace in faceMatrix:
        for currentVertex in currentFace:
                vertexDictOfTouchedFaces[currentVertex].append(currentFace)


    ##Create the dictionary for each uncovered face, will be removed from throughout the process
    vertexDictOfTouchingUncoveredFaces = copy.deepcopy(vertexDictOfTouchedFaces)

    vertexDictOfTouchedFacesEnding = {}
    for nextVertex in range(maxVert):
        vertexDictOfTouchedFacesEnding[nextVertex+1] = []
    
    ## Fill in the dictionary
    for currentFace in faceMatrix:
        for currentVertex in currentFace:
                vertexDictOfTouchedFacesEnding[currentVertex].append(currentFace)

    ###Create Dictionary Of Which Vertices a Single Vertex shares edges with
    vertexDictOfSharedEdges = {}

    for nextVertex in range(maxVert):
        vertexDictOfSharedEdges[nextVertex+1] = []


    rows, cols = (maxVert, maxVert)
    vertexSharedFacesCount = [[0 for i in range(cols)] for j in range(rows)]

    for currentVertex in vertexDictOfTouchedFaces:
       for currentFace in vertexDictOfTouchedFaces[currentVertex]:
           for vertexOnFace in currentFace:
               vertexSharedFacesCount[currentVertex-1][vertexOnFace-1] += 1
               if vertexSharedFacesCount[currentVertex-1][vertexOnFace-1] > 1 and vertexOnFace not in vertexDictOfSharedEdges[currentVertex]:
                       if vertexOnFace != currentVertex:
                           vertexDictOfSharedEdges[currentVertex].append(vertexOnFace)
    
    ##PUT THIS INSIDE LOOP ABOVE, SO TO ACCESS THE VALUE OF vertexOnFace
    ## Also, use number of faces each vertex is on to eliminate vertices pairing wiht self
    ##for x in vertexSharedFacesCount[currentVertex-1]:
        ##if x > 1:
            ##print(x, currentVertex)

    tempVertexDictOfSharedEdges = copy.deepcopy(vertexDictOfSharedEdges)


    #Once this removes an element from the dictionary, it doesn't check the next value. use temp dictionary
    for currentVertex in vertexDictOfSharedEdges:
        for connectedVertex in vertexDictOfSharedEdges[currentVertex]:
            if connectedVertex == currentVertex:
                tempVertexDictOfSharedEdges[currentVertex].remove(connectedVertex)

    vertexDictOfSharedEdges = copy.deepcopy(tempVertexDictOfSharedEdges)

    ###Vertex Shared Edges Ending
    vertexDictOfSharedEdgesEnding = {}

    for nextVertex in range(maxVert):
        vertexDictOfSharedEdgesEnding[nextVertex+1] = []


    rows, cols = (maxVert, maxVert)
    vertexSharedFacesCountEnding = [[0 for i in range(cols)] for j in range(rows)]
    #print(len(vertexSharedFacesCount)*len(vertexSharedFacesCount[0]))

    for currentVertex in vertexDictOfTouchedFacesEnding:
        #print(currentVertex, vertexDictOfTouchedFaces[currentVertex])
        for currentFace in vertexDictOfTouchedFacesEnding[currentVertex]:
            for vertexOnFace in currentFace:
                vertexSharedFacesCountEnding[currentVertex-1][vertexOnFace-1] += 1
                if vertexSharedFacesCountEnding[currentVertex-1][vertexOnFace-1] > 1 and vertexOnFace not in vertexDictOfSharedEdgesEnding[currentVertex]:
                        if vertexOnFace != currentVertex:
                            vertexDictOfSharedEdgesEnding[currentVertex].append(vertexOnFace)
    
    ##PUT THIS INSIDE LOOP ABOVE, SO TO ACCESS THE VALUE OF vertexOnFace
    ## Also, use number of faces each vertex is on to eliminate vertices pairing wiht self
    ##for x in vertexSharedFacesCount[currentVertex-1]:
        ##if x > 1:
            ##print(x, currentVertex)

    tempVertexDictOfSharedEdgesEnding = copy.deepcopy(vertexDictOfSharedEdgesEnding)
    #print(tempVertexDictOfSharedEdges)

    #Once this removes an element from the dictionary, it doesn't check the next value. use temp dictionary
    for currentVertex in vertexDictOfSharedEdgesEnding:
        for connectedVertex in vertexDictOfSharedEdgesEnding[currentVertex]:
            #print(currentVertex, connectedVertex)
            if connectedVertex == currentVertex:
                tempVertexDictOfSharedEdgesEnding[currentVertex].remove(connectedVertex)

    vertexDictOfSharedEdgesEnding = copy.deepcopy(tempVertexDictOfSharedEdgesEnding)
    ###Fill out matrix of vertex to vertex distances
    rows, cols = (maxVert, maxVert)
    vertexToVertexDistance = [[999 for i in range(cols)] for j in range(rows)]

    for i in range(0,maxVert):
        vertexToVertexDistance[i][i] = 0

    edgesAway = 1

    while np.max(vertexToVertexDistance) == 999:
        for vertex in vertexDictOfSharedEdgesEnding:
            for secondVertex in vertexDictOfSharedEdgesEnding:
                if vertexToVertexDistance[vertex-1][secondVertex-1] == edgesAway-1:
                    #print(secondVertex, " is ", edgesAway, " away")
                    for vertXAway in vertexDictOfSharedEdgesEnding[secondVertex]:
                        if vertexToVertexDistance[vertex-1][vertXAway-1] == 999:
                            vertexToVertexDistance[vertex-1][vertXAway-1] = edgesAway
        edgesAway += 1
  
    #print(vertexToVertexDistance)
    ####End of kevin's code

    for i in vertexToVertexDistance:
            print(i)


    vertArr = [(i +1) for i in range(np.max(faceMatrix))]

    maxDistanceDic = {}
    for solArr in list(combinations(vertArr,solutionSize)):
        distance = 0
        for vertPair in list(combinations(solArr,2)):
            distance += pow(vertexToVertexDistance[vertPair[0]-1][vertPair[1]-1],power)
        try:
            maxDistanceDic[distance].append(solArr)
        except KeyError:
            maxDistanceDic[distance] = []
            maxDistanceDic[distance].append(solArr)
    
    size = np.max([i for i in maxDistanceDic.keys()])    
    return size, maxDistanceDic[size]

def newDistanceSolver(faceMatrix, solutionSize, power, dimensions):
    listOfSolutions = []

    ###Start of kevins code
    maxVert = np.max(faceMatrix)

    vertexDictOfTouchedFaces = {}

    for nextVertex in range(maxVert):
        vertexDictOfTouchedFaces[nextVertex+1] = []
    
    ## Fill in the dictionary
    for currentFace in faceMatrix:
        for currentVertex in currentFace:
                vertexDictOfTouchedFaces[currentVertex].append(currentFace)
            
    #print(vertexDictOfTouchedFaces)


    ##Create the dictionary for each uncovered face, will be removed from throughout the process
    vertexDictOfTouchingUncoveredFaces = copy.deepcopy(vertexDictOfTouchedFaces)

    ##Create something that stores every vertex, and each other vertex it shares an edge with
    ## shares edge if it shares 2 faces
    ##Look in vertexDictOfTouchedFaces, keep count of each time each vertex appears. If > 1 and not the original, edge
    ##What to store in, dict doesn't seem to be working well, hard with arrays as values
    ## Dict for now
    
    
    vertexDictOfSharedEdges = {}

    for nextVertex in range(maxVert):
        vertexDictOfSharedEdges[nextVertex+1] = []



    rows, cols = (maxVert, maxVert)
    vertexSharedFacesCount = [[0 for i in range(cols)] for j in range(rows)]
    #print(len(vertexSharedFacesCount)*len(vertexSharedFacesCount[0]))



    for currentVertex in vertexDictOfTouchedFaces:
    
        #print(currentVertex, vertexDictOfTouchedFaces[currentVertex])
        for currentFace in vertexDictOfTouchedFaces[currentVertex]:
            for vertexOnFace in currentFace:
                vertexSharedFacesCount[currentVertex-1][vertexOnFace-1] += 1
                if vertexSharedFacesCount[currentVertex-1][vertexOnFace-1] > dimensions-2 and vertexOnFace not in vertexDictOfSharedEdges[currentVertex]:
                        if vertexOnFace != currentVertex:
                            vertexDictOfSharedEdges[currentVertex].append(vertexOnFace)
    
    ##PUT THIS INSIDE LOOP ABOVE, SO TO ACCESS THE VALUE OF vertexOnFace
    ## Also, use number of faces each vertex is on to eliminate vertices pairing wiht self
    ##for x in vertexSharedFacesCount[currentVertex-1]:
        ##if x > 1:
            ##print(x, currentVertex)
            


    #print(vertexSharedFacesCount)
    #print(vertexDictOfSharedEdges)

    tempVertexDictOfSharedEdges = copy.deepcopy(vertexDictOfSharedEdges)
    #print(tempVertexDictOfSharedEdges)

    #Once this removes an element from the dictionary, it doesn't check the next value. use temp dictionary
    for currentVertex in vertexDictOfSharedEdges:
        for connectedVertex in vertexDictOfSharedEdges[currentVertex]:
            #print(currentVertex, connectedVertex)
            if connectedVertex == currentVertex:
                tempVertexDictOfSharedEdges[currentVertex].remove(connectedVertex)
                #print("removed", connectedVertex)
            
    #print(vertexDictOfSharedEdges)

    vertexDictOfSharedEdges = copy.deepcopy(tempVertexDictOfSharedEdges)

    rows, cols = (maxVert, maxVert)
    vertexToVertexDistance = [[999 for i in range(cols)] for j in range(rows)]
    #print(vertexToVertexDistance)

    for i in range(0,maxVert):
        vertexToVertexDistance[i][i] = 0

    #print( vertexToVertexDistance)

    edgesAway = 1

    while np.max(vertexToVertexDistance) == 999:
        for vertex in vertexDictOfSharedEdges:
            for secondVertex in vertexDictOfSharedEdges:
                if vertexToVertexDistance[vertex-1][secondVertex-1] == edgesAway-1:
                    #print(secondVertex, " is ", edgesAway, " away")
                    for vertXAway in vertexDictOfSharedEdges[secondVertex]:
                        if vertexToVertexDistance[vertex-1][vertXAway-1] == 999:
                            vertexToVertexDistance[vertex-1][vertXAway-1] = edgesAway
        edgesAway += 1
    #print(vertexToVertexDistance)

    ###End of kevins code

    
    vertArr = [(i +1) for i in range(np.max(faceMatrix))]

    maxDistanceDic = {}
    for solArr in list(combinations(vertArr,solutionSize)):
        distance = 1
        for vertPair in list(combinations(solArr,2)):
            distance *= pow(vertexToVertexDistance[vertPair[0]-1][vertPair[1]-1],power)
        try:
            maxDistanceDic[distance].append(solArr)
        except KeyError:
            maxDistanceDic[distance] = []
            maxDistanceDic[distance].append(solArr)
    
    size = np.max([i for i in maxDistanceDic.keys()])    
    return size, maxDistanceDic[size]


def redundancy(vertArr, faceMatrix):
    redund = 0
    #check if it is a solution
    if not solChecker(vertArr,faceMatrix):
        return -1
    #loops through each face
    for face in faceMatrix:
        #creates a holing val
        numOfVertsToching = 0
        #loops through vertices
        for vert in vertArr:
            #if the face is touching the vert increase holding var
            if vert in face:
                numOfVertsToching += 1
        #if the holding var is greater then 1 adds how many times the face is redundent
        if numOfVertsToching > 1:
            redund += 1
    return redund

def solChecker(vertArr, faceMatrix):
    #loops through each face
    for face in faceMatrix:
        #makes a list comperhension of all the verts in vert array that it is toching 
        #then checks if the length is 0
        if len([i for i in vertArr if i in face]) == 0:
            #if it is then it returns false
            return False
    #if it runs through every face then it is true
    return True

if __name__ == "__main__":
    with open('code/faceMatrices/24cell.txt') as csvFile:
        #code for taking the face matrix input from txt file
        csvReader = csv.reader(csvFile, delimiter=',')
        faceMatrix = []
        for row in csvReader:
            holdingArr = []
            for i in row:
                holdingArr.append(int(i))
            faceMatrix.append(holdingArr)
        
        #Finds the max index of the vertex
        maxVertIndex = np.max(faceMatrix)
        
        #finding all the solutions for coverage
        coverageSolutionList = bruteForceCoverSolution(faceMatrix,maxVertIndex)

        #Prints coverage solutions
        print("Coverage Solution")
        print(coverageSolutionList)

        #finding all size solutions for the distance problem to the specified power
        DistanceSolTuple = newDistanceSolver(faceMatrix, len(coverageSolutionList[0]),1,4)

        #prints out the distance solutions at the largest distance
        print("Distance Solution")
        print(DistanceSolTuple[0])
        for sol in DistanceSolTuple[1]:
            print(sol)
        
        

        #prints out redundency for the coverage solutions
        print("redundancy of the coverage solutions")
        for sol in coverageSolutionList:
            redund = redundancy(sol, faceMatrix)
            print("{0}: Redundency = {1}".format(sol, redund)) 

        
          



        