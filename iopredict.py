from __future__ import division
import shapeFile as sF
import matplotlib.pyplot as plt
import matplotlib.colors as cl

import random
import numpy as np
import math
from scipy.stats import ks_2samp

#return mean, std, max, min
def caDistribution(ioDict):
    #according to the figuire, the output time is very similar, caculate 
    ioList = []
    for fileName in ioDict.keys():
        for domain in ioDict[fileName].keys():
            ioList += ioDict[fileName][domain]
    data=np.array(ioList).astype(np.float)
    return (np.mean(data), np.std(data), np.max(data), np.min(data))

def drawIODomain(ioDict, domainRange, meanValue, stdValue, maxValue, minValue, subplots, subplotIdx):

    #cacluate color for each file
    colorV={}
    for filename in ioDict.keys():
        colorV[filename]=(random.uniform(0,0.99), random.uniform(0,0.95), random.uniform(0,0.92))
    
    for i in range(0, domainRange):
        plt.sca(subplots[i+subplotIdx])#choose subpic
        plt.title("domain%d" %(i+1))
        plt.ylim(minValue, maxValue)
        if i==0 :
            plt.ylabel('Consumed Time(s)')
        
        #draw per file
        for fileName in sorted(ioDict.keys()):
            xAxle=range(0, len(ioDict[fileName][str(i+1)]))
            plt.plot(xAxle, ioDict[fileName][str(i+1)], color=colorV[fileName])

  #  plt.draw()

def drawIODist(subplots, data, domainRange, meanV, stdV, coeff):
    ##plot the gaussian distribution
    maxCoeff = 4.1
    setp = 0.05
    xAxle = np.arange(meanV-stdV*maxCoeff, meanV+stdV*maxCoeff, setp)
    yAxle = []
    for x in xAxle:
        yAxle.append(1/(math.sqrt(2*math.pi)*stdV)*math.exp(-math.pow(x-meanV, 2)/(2*math.pow(stdV,2))))
    plt.sca(subplots[domainRange])#after the domain chart, first sub chart
    plt.title("Consumed Time Distribution")
    plt.plot(xAxle, yAxle)
    ##plot the tru distribution
    x1 = sorted(data)
    yAxle = []
    xAxle = []
    roundNum = 1
    for x in x1:
        if not xAxle:
            xAxle.append(round(x,roundNum))
            yAxle.append(1)
        elif round(x, roundNum) == xAxle[-1]:
            yAxle[-1] += 1
        else:
            xAxle.append(round(x,roundNum))
            yAxle.append(1)
    plt.sca(subplots[domainRange]) # choose pciture
    plt.plot(xAxle, np.array(yAxle).astype(np.float)/len(data), 'ro')

    #Draw two side line
    yMax = 1/(math.sqrt(2*math.pi)*stdV)*math.exp(-math.pow(meanV+stdV*coeff-meanV, 2)/(2*math.pow(stdV,2)))
    yAxle = np.arange(0, yMax, yMax/20)
    xAxle = [meanV+stdV*coeff]*20

    plt.plot(xAxle, yAxle, color='#000000')
    xAxle = [meanV-stdV*coeff]*20
    plt.plot(xAxle, yAxle, color='#000000')



