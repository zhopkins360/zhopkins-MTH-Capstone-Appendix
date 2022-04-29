import numpy as np
import pandas as pd

prevArr = []
currArr = []
def ncelltableCalc(ndim):
    #creating th
    #starting if for recurrsion
    if ndim == 0:
        return [1]

    prevArr = ncelltableCalc(ndim - 1)
    #sets the 0-cell
    currArr = [0] * (ndim + 1)
    try:
        currArr[0] = prevArr[0] * 2
    except(IndexError): 
        currArr.append(prevArr[0] * 2)
    #appends a 0 to add the next dim
    prevArr.append(0)
    #loops through each of the current dim cells and changes them
    for i in range(1,ndim+1):
        #print(str(i) + " "+str(len(currArr)) +" "+str(len(prevArr)))
        currArr[i] = 2 * prevArr[i] + prevArr[i-1] 
    #returns the current dim array
    return currArr


if __name__ == "__main__":
    ndim = input("What dim of a square would you like to see?")
    holderVar = ncelltableCalc(int(ndim))
    print("index | #n-cells")
    for i in range(0,len(holderVar)):
        print(str(i) + (" "*8) + str(holderVar[i]))