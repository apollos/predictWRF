from __future__ import division
import shapeFile as sF
import random
from numpy import *
import math
import matplotlib.pyplot as plt
import writeTrainingResult as wTR
import regression 
import os.path
import myUtils
import myDebug

files = sF.listAllFiles("/home/yu/workspace/Data/train")
trainDataList = sF.shapeWrfComputingfile(files)
if not trainDataList:
    print("%s  %d: Get profiling information from %s failed." %(myDebug.file(), myDebug.line(), files))
    exit(1)
#Get test data, we need check together
files = sF.listAllFiles("/home/yu/workspace/Data/test")
testDataList = sF.shapeWrfComputingfile(files)
if not testDataList:
    print("%s  %d: Get profiling information from %s failed." %(myDebug.file(), myDebug.line(), testFile))
    exit(1)
#for i in range(0,2):#0 for task 0 and 1 for other tasks
#The list is sperated to two part, [0] save all task 0 job information, task 1 save all other tasks
#generate traing dataset
#task 0 first
'''
print "%d, %d, %d" % (len(trainDataList), len(trainDataList[0]), len(trainDataList[1]))
print trainDataList
print "==========================="
print "%d, %d, %d" % (len(testDataList), len(testDataList[0]), len(testDataList[1]))
print testDataList
exit(1)
'''

for taskIdx in range(1,2):
    xMat, yMat = myUtils.getXandYMatfromList(trainDataList[taskIdx], 2)
    xTMat, yTMat = myUtils.getXandYMatfromList(testDataList[taskIdx], 2)
    xMat = mat(xMat, dtype = float)
    xTMat = mat(xTMat, dtype = float)
    yMat = mat(yMat, dtype = float)
    yTMat = mat(yTMat, dtype = float)
    #Regularize the matrix 
    xMat[:, 1:], xMeans, xStd = regression.regularize(xMat[:, 1:])         
    xTMat[:, 1:] = (xTMat[:, 1:] - xMeans)/xStd

    print "Start compute taskIdx %d:" % taskIdx
    
    for yIdx in range(0, 2): #caculate computing result and then communication result
        bestKList = []#we may meet sigular case while we predict, so we save 10 good k and try 10 times. [lowestError, bestK]
        invalidKNum = 0
        invalidKMin = inf
        invalidKMax = 0.009

        yMatTmp = yMat[:, yIdx]     
        yTMatTmp = yTMat[:, yIdx]     
        
        for k in arange(5, 0.09, -0.1):##find best k              
            yAssume = regression.lwlrTest(xTMat,xMat,yMatTmp.T,k)
            print k
            if yAssume.all() == 0:
                #print("%s  %d: regression.lwlr failed by k = %f." %(myDebug.file(), myDebug.line(), k))
                invalidKNum += 1
                if k > invalidKMax:
                    invalidKMax = k
                if k < invalidKMin:
                    invalidKMin = k
                continue        
            #transfer Mat to list
            yTList = yTMatTmp.reshape(-1).tolist() 
            yTList = [j for i in yTList for j in i]   
            rssE = regression.rssError(yTList, yAssume)            
            if len(bestKList) == 0:
                bestKList.insert(0, [rssE, k])
            else:
                for idx in range(0, len(bestKList)):
                    if rssE < bestKList[idx][0]:
                        bestKList.insert(idx, [rssE, k])
                        if len(bestKList) > 50: #save 50 top k
                            bestKList.pop()
                        break
        print bestKList
        




