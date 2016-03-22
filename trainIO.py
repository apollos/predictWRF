from __future__ import division
import shapeFile as sF
import random
import numpy as np
import math
from scipy.stats import ks_2samp
import iopredict as ioP
import matplotlib.pyplot as plt
import writeTrainingResult as wTR


keyWords = ["wrfout", "wrfinput"]
IOfeatures = {}
figureIdx = 1
for keyWord in keyWords:
    files = sF.listAllFiles("/home/yu/workspace/Data/train")
    ioDict = sF.shapeWrfIOfile(files, "0000", keyWord)
    if not ioDict:
        print("Generate ioDict failed from %s" % (fiels))
        return
    (meanV, stdV, maxV, minV) = ioP.caDistribution(ioDict)
    
    domain=range(0,4)
    subplotIdx = 0
    if keyWord == "wrfout":
        fig = plt.figure(figureIdx, figsize=(16,12)) # create pciture
        picRow = round(math.sqrt(len(domain)) + 1)
        subplots = range(0, int(picRow*(picRow-1)))
        for i in range(0, len(subplots)):
            subplots[i] = plt.subplot(picRow, picRow-1 , i+1)
        ioP.drawIODomain(ioDict, len(domain), meanV, stdV, maxV, minV, subplots, subplotIdx)
        subplotIdx += len(domain)
    else:
        fig = plt.figure(figureIdx)
        picRow = 1
        subplots = range(0, 1)
        subplots[0] = plt.subplot(1,1,1)
    figureIdx +=1
    fig.suptitle(keyWord)    
    
    #check other output file, whether they are same distribution
    print("======Test data set===============")
    testFiles = "/home/yu/workspace/Data/test"
    files = sF.listAllFiles(testFiles)
    ioDict = sF.shapeWrfIOfile(files, "0000", keyWord)
    ioList = []
    for fileName in ioDict.keys():
        for domain in ioDict[fileName].keys():
            ioList += ioDict[fileName][domain]
    testData=np.array(ioList).astype(np.float)
  
    coeff = 1.96
    step = 0.01
    totalData = len(testData)
    count = totalData
    while(count/totalData >= 0.05):        
        for i in testData:
            if i <meanV+coeff*stdV and i >meanV - coeff*stdV:
                count -=1
        if count/totalData >= 0.05 :
            coeff += step
            count = totalData
    
    print("Total out of range number is %d, total %d and the propability is %f and coeff is %f" % (count, totalData, count/totalData, coeff))
    ioP.drawIODist(subplots, testData, subplotIdx, meanV, stdV, coeff)
    IOfeatures[keyWord] = {"meanV":meanV, "stdV":stdV, "coeff":coeff}
wTR.writeIOTraingResult(IOfeatures)
    
plt.show()
