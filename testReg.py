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

fr = open("/home/yu/workspace/machine-learning-class/ex1/ex1data2.txt")
xMat = []
yMat = []
for line in fr.readlines():
    tmpEle = line.split(',')
    xMat.append([1, tmpEle[0], tmpEle[1]])
    yMat.append([tmpEle[2]])

bestKList = [10]#[0.07, 0.3, 0.1, 0.7, 3, 10, 28, 40, 60, 80, 100]#[100, 80, 60, 40, 28, 10, 3, 0.7, 0.3, 0.07, 0.01]    

xCheckMat = mat([1, 1650, 3], dtype = float)        
xMat = mat(xMat, dtype = float)        
yMat = mat(yMat, dtype = float)

#Regularize the matrix 
xMat[:, 1:], xMeans, xStd = regression.regularize(xMat[:, 1:])         
xCheckMat[:, 1:] = (xCheckMat[:, 1:] - xMeans)/xStd
for kElement in bestKList:
    taskPredict = 0
    #get the result for cared data
    wr = regression.lwlr(xCheckMat, xMat,yMat.T,kElement)
    #wr = regression.standRegres(xMat,yMat.T)
    if (wr != None):
        print wr
        taskPredict = xCheckMat * wr
        print taskPredict
        break                       
    
