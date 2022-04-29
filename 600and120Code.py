import copy
from click import version_option
import numpy as np
from itertools import combinations
import csv


def distanceCalForGivenSol(faceMatrix, solutions, power, dimensions):
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
    for solArr in solutions:
        distance = 1
        for vertPair in list(combinations(solArr,2)):
            distance *= pow(vertexToVertexDistance[vertPair[0]-1][vertPair[1]-1],power)
        try:
            maxDistanceDic[distance].append(solArr)
        except KeyError:
            maxDistanceDic[distance] = []
            maxDistanceDic[distance].append(solArr)
    
    return maxDistanceDic

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
    with open(filePath) as csvFile:
        #code for getting the solutions{} from csv
        csvReader = csv.reader(csvFile, delimiter=',')
        solutions = []

        for row in csvReader:
            holdingArr = []
            for i in row:
                holdingArr.append(int(i))
            solutions.append(holdingArr)

        #print(len(solutions[0]))

        #code for getting the faceMatrix from a csv
        with open(filePath) as faceCsvFile:
            csvReader = csv.reader(faceCsvFile, delimiter=',')
            faceMatrix = []

            for row in csvReader:
                holdingArr = []
                for i in row:
                    holdingArr.append(int(i))
                faceMatrix.append(holdingArr)
            #print(len(faceMatrix))

            #for sol in solutions:
                #print("sol : {0} , Redundency : {1}".format(sol,redundancy(sol, faceMatrix)))
            
            for dist,sol in distanceCalForGivenSol(faceMatrix,solutions,2,4).items():
                print("sol : {0} , Distance : {1}".format(sol,dist))
            

        
        
