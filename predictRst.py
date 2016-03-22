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

files = sF.listAllFiles("Data/train")
trainDataList = sF.shapeWrfComputingfile(files)
if not trainDataList:
    print("%s  %d: Get profiling information from %s failed." %(myDebug.file(), myDebug.line(), files))
    exit(1)

#for i in range(0,2):#0 for task 0 and 1 for other tasks
#The list is sperated to two part, [0] save all task 0 job information, task 1 save all other tasks
#generate traing dataset
#task 0 first
'''
print "%d, %d, %d" % (len(trainDataList), len(trainDataList[0]), len(trainDataList[1]))
print trainDataList
print "==========================="
exit(1)
'''
bestKList = [28, 10, 3, 0.7, 0.3, 0.07, 0.01, 40, 60, 80, 100]#[0.6, 0.8, 0.7, 0.9, 1, 0.5, 0.4, 0.2, 1.1, 1.2, 1.3]#[100, 80, 60, 40, 28, 10, 3, 0.7, 0.3, 0.07, 0.01]    
predictHourList = [6, 180]
predictTaskSizeList = range(40, 440, 20)
predictHours = predictHourList[1]
predictList = []
for tTSize in predictTaskSizeList:
    taskX = int(sqrt(tTSize))
    while(tTSize % taskX != 0):
        taskX -= 1
    taskY = tTSize/taskX
    xCheckMat = mat([myUtils.getConstantValue(), tTSize, taskX, taskY, predictHours], dtype = float)

    preDictPerTask = []
    for taskIdx in range(1,2):
        xMat, yMat = myUtils.getXandYMatfromList(trainDataList[taskIdx], 2)
        xMat = mat(xMat, dtype = float)        
        yMat = mat(yMat, dtype = float)

        #Regularize the matrix 
        xMat[:, 1:], xMeans, xStd = regression.regularize(xMat[:, 1:])         
        xCheckMat[:, 1:] = (xCheckMat[:, 1:] - xMeans)/xStd
        
        preDictPerComponent = []
        for yIdx in range(0, 2): #caculate computing result and then communication result
            yMatTmp = yMat[:, yIdx]       
            
            taskPredict = 0
            for kElement in bestKList:
                taskPredict = 0
                #get the result for cared data
                wr = regression.lwlr(xCheckMat, xMat,yMatTmp.T,kElement)
                #wr = regression.standRegres(xMat,yMatTmp.T)
                if (wr != None):
                    #print wr
                    taskPredict = xCheckMat * wr
                    #print taskPredict
                    #print "Task Size: %d, Predict Hours: %d Result[%d] is %f with k %f" % (tTSize, predictHours, yIdx, taskPredict, kElement)
                    #print wr
                    break                       
            if taskPredict != 0:
                tmp = taskPredict.reshape(-1).tolist() #sum only used for get the value but not the matrix
                tmp = [j for i in tmp for j in i]
                preDictPerComponent.extend(tmp) 
            else:
                print "Error! Task Size: %d, Predict Hours: %d Task %d can not get predict value" % (tTSize, predictHours, yIdx)
        
        #preDictPerTask.append(sum(preDictPerComponent))
        preDictPerTask.extend(preDictPerComponent)
    #predictList.append([tTSize, max(preDictPerTask)])
    endIdx = int(len(preDictPerTask)/2)
    for i in range(0, endIdx):
        predictList.append([tTSize, preDictPerTask[i*2], preDictPerTask[i*2+1]])

print predictList
